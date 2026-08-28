# -*- coding: utf-8 -*-
"""TCD5: UsageCode = OUSG.ID da extração DESTE projeto. Não inventa ID."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib_tcd import (
    arg_config,
    batch_size,
    load_config,
    map_uso,
    nval,
    require_projeto,
    saida_camada,
    sql_num,
    sql_str,
    write_batches,
)

import pandas as pd


def load_ousg(path: Path):
    ext = pd.read_excel(path, sheet_name=0, dtype=object)
    col_id = "ID_Interno" if "ID_Interno" in ext.columns else "OUSG_ID"
    col_uso = "Codigo" if "Codigo" in ext.columns else "Utilizacao"
    by_exact, by_norm = {}, {}
    from lib_tcd import norm_uso

    for _, r in ext.iterrows():
        uso = nval(r.get(col_uso) or r.get("Usage"))
        oid = pd.to_numeric(r.get(col_id) or r.get("ID"), errors="coerce")
        if not uso or pd.isna(oid):
            continue
        oid = int(oid)
        by_exact[uso] = min(oid, by_exact.get(uso, oid))
        n = norm_uso(uso)
        if n not in by_norm or oid < by_norm[n][1]:
            by_norm[n] = (uso, oid)
    return by_exact, by_norm


def main():
    cfg = load_config(arg_config())
    nome = require_projeto(cfg)
    ousg_path = (cfg.get("ousg") or {}).get("extracao")
    if not ousg_path:
        raise SystemExit("ousg.extracao obrigatório (export Q03 DESTE CompanyDB)")
    src5 = saida_camada(cfg, "TCD5") / "TCD5_CARGA.xlsx"
    if not src5.exists():
        raise SystemExit(
            f"{src5} não existe. Monte TCD5_CARGA deste projeto com "
            "AbsId_TCD3, UsageCode (ou Usage_texto), TaxCode, ExpTaxCode, PurTaxCode."
        )
    otcd = (cfg.get("otcd") or {}).get("abs_id")
    if not otcd:
        raise SystemExit("otcd.abs_id obrigatório (Q01 neste CompanyDB).")
    otcd = int(otcd)
    by_exact, by_norm = load_ousg(Path(ousg_path))
    df = pd.read_excel(src5, sheet_name=0)
    inserts, bloqueados = [], []
    batch = batch_size(cfg)
    absid = 0
    for _, r in df.iterrows():
        tcd3 = int(r["AbsId_TCD3"])
        oid = r.get("UsageCode")
        if pd.isna(oid) or oid == "":
            oid, sap, como = map_uso(nval(r.get("Usage_texto")), by_exact, by_norm)
            if oid is None:
                bloqueados.append({"AbsId_TCD3": tcd3, "motivo": como, "Usage_texto": r.get("Usage_texto")})
                continue
        else:
            oid = int(oid)
        tax, exp, pur = nval(r.get("TaxCode")), nval(r.get("ExpTaxCode")), nval(r.get("PurTaxCode"))
        absid += 1
        inserts.append(
            "INSERT INTO TCD5 "
            '("AbsId","TcdId","Tcd3Id","UsageCode","TaxCode","ExpTaxCode","PurTaxCode") '
            f"VALUES ({absid},{otcd},{tcd3},{sql_num(oid)},{sql_str(tax)},{sql_str(exp)},{sql_str(pur)});"
        )
    out = saida_camada(cfg, "TCD5")
    header = [
        f"-- TCD5 projeto={nome}. UsageCode=OUSG.ID desta base.",
        f"-- Gerados {len(inserts)}. Bloqueados {len(bloqueados)} (sem OUSG — nao inventar).",
        "",
    ]
    write_batches(inserts, out, "TCD5_INSERT", batch, header)
    if bloqueados:
        pd.DataFrame(bloqueados).to_excel(out / "BLOQUEADOS.xlsx", index=False)
    print(nome, "TCD5", len(inserts), "bloqueados", len(bloqueados))


if __name__ == "__main__":
    main()
