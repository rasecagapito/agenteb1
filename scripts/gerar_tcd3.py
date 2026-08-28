# -*- coding: utf-8 -*-
"""TCD3: vigências desta carga.

Três modos, nesta ordem de precedência:

1. `TCD3/TCD3_CARGA.xlsx` existe  → N vigências por TCD2 (AbsId_TCD2, EfctFrom, EfctTo).
2. `tcd3.modo_teste: true`        → 1 período aberto por TCD2, a partir de `test_from`.
3. produção 1:1                   → EfctFrom/EfctTo da própria grade TCD2.

A grade TCD2 vem sempre de `ler_grade_tcd2`, com o mesmo filtro de
`skip_prioridades`. Ler o xlsx direto desalinharia Tcd2Id do AbsId realmente
inserido na TCD2.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib_tcd import (
    arg_config,
    batch_size,
    exportar_grade,
    ler_grade_tcd2,
    load_config,
    require_projeto,
    saida_camada,
    sql_str,
    to_date,
    write_batches,
)

import pandas as pd


def _insert(absid: int, otcd: int, tcd2: int, dfrom, dto) -> str:
    return (
        "INSERT INTO TCD3 "
        '("AbsId","TcdId","Tcd2Id","EfctFrom","EfctTo","TaxCode") '
        f"VALUES ({absid},{otcd},{tcd2},{sql_str(dfrom.isoformat())},"
        f"{sql_str(dto.isoformat()) if dto else 'NULL'},NULL);"
    )


def _periodos_do_arquivo(src: Path, validos: set[int]) -> list[tuple[int, object, object]]:
    """Lê TCD3_CARGA.xlsx e devolve (Tcd2Id, EfctFrom, EfctTo) validado e ordenado.

    Erra em vez de gerar parcial: período sobreposto ou segundo período aberto na
    mesma TCD2 tornam a determinação ambígua — o SAP não sabe qual regra aplicar.
    """
    df = pd.read_excel(src, sheet_name=0)
    faltando = [c for c in ("AbsId_TCD2", "EfctFrom") if c not in df.columns]
    if faltando:
        raise SystemExit(f"{src.name} sem coluna(s) {faltando}. Ver scripts/README.md.")

    linhas, sem_data, fora, invertidas = [], [], [], []
    for i, r in df.iterrows():
        excel_ln = i + 2  # 1 = cabeçalho
        tcd2 = pd.to_numeric(r.get("AbsId_TCD2"), errors="coerce")
        if pd.isna(tcd2) or int(tcd2) not in validos:
            fora.append((excel_ln, r.get("AbsId_TCD2")))
            continue
        dfrom = to_date(r.get("EfctFrom"))
        dto = to_date(r.get("EfctTo")) if "EfctTo" in df.columns else None
        if dfrom is None:
            sem_data.append(excel_ln)
            continue
        if dto is not None and dto < dfrom:
            invertidas.append(excel_ln)
            continue
        linhas.append((int(tcd2), dfrom, dto))

    if fora:
        raise SystemExit(
            f"{src.name}: AbsId_TCD2 inexistente na grade desta carga (linha, valor) "
            f"{fora[:20]}. Use os AbsId de TCD2_GRADE.xlsx — prioridade skipada não entra."
        )
    if sem_data:
        raise SystemExit(f"{src.name}: EfctFrom vazio ou inválido nas linhas {sem_data[:20]}.")
    if invertidas:
        raise SystemExit(f"{src.name}: EfctTo anterior a EfctFrom nas linhas {invertidas[:20]}.")

    linhas.sort(key=lambda x: (x[0], x[1]))
    for tcd2 in {l[0] for l in linhas}:
        seq = [l for l in linhas if l[0] == tcd2]
        for (_, af, at), (_, bf, _bt) in zip(seq, seq[1:]):
            if at is None:
                raise SystemExit(
                    f"{src.name}: TCD2 {tcd2} tem período aberto ({af}) e outro depois ({bf}). "
                    "Só a última vigência pode ficar sem EfctTo."
                )
            if at >= bf:
                raise SystemExit(
                    f"{src.name}: períodos sobrepostos na TCD2 {tcd2} — "
                    f"{af}..{at} e {bf}... A determinação ficaria ambígua."
                )
    return linhas


def main():
    cfg = load_config(arg_config())
    nome = require_projeto(cfg)
    t3 = cfg.get("tcd3") or {}
    modo_teste = bool(t3.get("modo_teste", True))

    otcd = (cfg.get("otcd") or {}).get("abs_id")
    if not otcd:
        raise SystemExit("otcd.abs_id obrigatório (Q01 neste CompanyDB). Não assumir 1.")
    otcd = int(otcd)

    df = ler_grade_tcd2(cfg)
    validos = set(df["AbsId"].astype(int))
    out = saida_camada(cfg, "TCD3")
    src = out / "TCD3_CARGA.xlsx"
    rows, grade = [], []

    if src.exists():
        for absid, (tcd2, dfrom, dto) in enumerate(_periodos_do_arquivo(src, validos), start=1):
            rows.append(_insert(absid, otcd, tcd2, dfrom, dto))
            grade.append({"AbsId": absid, "AbsId_TCD2": tcd2,
                          "EfctFrom": dfrom.isoformat(),
                          "EfctTo": dto.isoformat() if dto else None})
        sem_periodo = sorted(validos - {g["AbsId_TCD2"] for g in grade})
        if sem_periodo:
            raise SystemExit(
                f"{src.name}: TCD2 sem nenhuma vigência: {sem_periodo[:20]}. "
                "Toda TCD2 inserida precisa de ao menos uma TCD3."
            )
        note = f"N vigencias por TCD2, de {src.name}"
    elif modo_teste:
        test_from = to_date(t3.get("test_from"))
        if test_from is None:
            raise SystemExit(
                "tcd3.test_from obrigatório nesta carga (combinar data com o cliente). "
                "Não copiar data de outro nome."
            )
        for _, r in df.iterrows():
            absid = int(r["AbsId"])
            rows.append(_insert(absid, otcd, absid, test_from, None))
            grade.append({"AbsId": absid, "AbsId_TCD2": absid,
                          "EfctFrom": test_from.isoformat(), "EfctTo": None})
        note = f"TESTE 1 periodo aberto {test_from.isoformat()} EfctTo=NULL TaxCode=NULL"
    else:
        if "EfctFrom" not in df.columns:
            raise SystemExit(
                "Produção 1:1 exige a coluna EfctFrom em TCD2_CARGA.xlsx. "
                "Para várias vigências na mesma combinação, monte TCD3_CARGA.xlsx "
                "(AbsId_TCD2, EfctFrom, EfctTo) — ver scripts/README.md."
            )
        sem_data, invertidas = [], []
        for _, r in df.iterrows():
            absid = int(r["AbsId"])
            dfrom = to_date(r.get("EfctFrom"))
            dto = to_date(r.get("EfctTo")) if "EfctTo" in df.columns else None
            if dfrom is None:
                sem_data.append(absid)
                continue
            if dto is not None and dto < dfrom:
                invertidas.append(absid)
                continue
            rows.append(_insert(absid, otcd, absid, dfrom, dto))
            grade.append({"AbsId": absid, "AbsId_TCD2": absid,
                          "EfctFrom": dfrom.isoformat(),
                          "EfctTo": dto.isoformat() if dto else None})
        if sem_data:
            raise SystemExit(
                f"EfctFrom vazio ou inválido nas linhas TCD2 {sem_data[:20]}"
                f"{' ...' if len(sem_data) > 20 else ''} — corrigir a grade, não gerar parcial."
            )
        if invertidas:
            raise SystemExit(f"EfctTo anterior a EfctFrom nas linhas TCD2 {invertidas[:20]}.")
        abertos = sum(1 for g in grade if g["EfctTo"] is None)
        note = f"PRODUCAO 1:1 datas da grade TCD2. {abertos} periodo(s) aberto(s)"

    header = [
        f"-- TCD3 carga={nome}. {note}.",
        "-- MI: TaxCode NULL. Nunca EfctTo 2099-12-31.",
        f"-- COUNT esperado = {len(rows)}",
        "",
    ]
    write_batches(rows, out, "TCD3_INSERT", batch_size(cfg), header)
    g = exportar_grade(pd.DataFrame(grade), out, "TCD3_GRADE")
    print(nome, "TCD3", len(rows), note)
    print("grade numerada:", g.name, "— use AbsId dela na TCD5_CARGA")


if __name__ == "__main__":
    main()
