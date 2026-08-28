# -*- coding: utf-8 -*-
"""TCD3: teste = 1 período aberto por TCD2; produção = datas da grade desta carga.

Lê a MESMA grade que a TCD2 (`ler_grade_tcd2`), com o mesmo filtro de
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
    ler_grade_tcd2,
    load_config,
    require_projeto,
    saida_camada,
    sql_str,
    to_date,
    write_batches,
)


def _insert(absid: int, otcd: int, tcd2: int, dfrom, dto) -> str:
    return (
        "INSERT INTO TCD3 "
        '("AbsId","TcdId","Tcd2Id","EfctFrom","EfctTo","TaxCode") '
        f"VALUES ({absid},{otcd},{tcd2},{sql_str(dfrom.isoformat())},"
        f"{sql_str(dto.isoformat()) if dto else 'NULL'},NULL);"
    )


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
    rows = []

    if modo_teste:
        test_from = to_date(t3.get("test_from"))
        if test_from is None:
            raise SystemExit(
                "tcd3.test_from obrigatório nesta carga (combinar data com o cliente). "
                "Não copiar data de outro nome."
            )
        for _, r in df.iterrows():
            absid = int(r["AbsId"])
            rows.append(_insert(absid, otcd, absid, test_from, None))
        note = f"TESTE 1 periodo aberto {test_from.isoformat()} EfctTo=NULL TaxCode=NULL"
    else:
        if "EfctFrom" not in df.columns:
            raise SystemExit(
                "Produção exige a coluna EfctFrom em TCD2_CARGA.xlsx (uma vigência por "
                "combinação, datas DESTA planilha). EfctTo é opcional: vazio = período aberto. "
                "Não copiar períodos de outro nome."
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
        if sem_data:
            raise SystemExit(
                f"EfctFrom vazio ou inválido nas linhas TCD2 {sem_data[:20]}"
                f"{' ...' if len(sem_data) > 20 else ''} — corrigir a grade, não gerar parcial."
            )
        if invertidas:
            raise SystemExit(f"EfctTo anterior a EfctFrom nas linhas TCD2 {invertidas[:20]}.")
        abertos = sum(1 for x in rows if x.endswith("NULL,NULL);"))
        note = f"PRODUCAO datas da grade. {abertos} periodo(s) aberto(s)"

    out = saida_camada(cfg, "TCD3")
    header = [
        f"-- TCD3 carga={nome}. {note}.",
        "-- MI: TaxCode NULL. Nunca EfctTo 2099-12-31.",
        f"-- COUNT esperado = {len(rows)} (= COUNT TCD2 desta carga)",
        "",
    ]
    write_batches(rows, out, "TCD3_INSERT", batch_size(cfg), header)
    print(nome, "TCD3", len(rows), "teste" if modo_teste else "producao")


if __name__ == "__main__":
    main()
