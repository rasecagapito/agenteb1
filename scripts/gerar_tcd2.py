# -*- coding: utf-8 -*-
"""Gera TCD2 INSERT a partir de TCD2_CARGA.xlsx DESTE projeto (não de outro nome)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib_tcd import arg_config, load_config, require_projeto, saida_camada, sql_str, nval

import pandas as pd


def lit(v):
    if v is None or (isinstance(v, float) and pd.isna(v)):
        return "NULL"
    s = nval(v)
    if s is None:
        return "NULL"
    if s.endswith(".0") and s.replace(".", "", 1).replace("-", "", 1).isdigit():
        s = s[:-2]
    return sql_str(s)


def main():
    cfg = load_config(arg_config())
    nome = require_projeto(cfg)
    skip = set(int(x) for x in (cfg.get("skip_prioridades") or []))
    src = saida_camada(cfg, "TCD2") / "TCD2_CARGA.xlsx"
    if not src.exists():
        raise SystemExit(
            f"{src} não existe. Monte a grade TCD2 DESTE projeto ({nome}) "
            "com colunas Prioridade, AbsId_TCD1, DispOrder, KeyFld_1_V..5_V."
        )
    df = pd.read_excel(src, sheet_name=0)
    if "Prioridade" in df.columns:
        df = df[~df["Prioridade"].isin(skip)].copy()
    df = df.sort_values(["Prioridade", "DispOrder"] if "DispOrder" in df.columns else df.columns[0]).reset_index(drop=True)

    rows = []
    for i, r in df.iterrows():
        absid = i + 1
        tcd1 = int(r["AbsId_TCD1"])
        disp = int(r["DispOrder"]) if "DispOrder" in df.columns else absid
        v1, v2, v3, v4, v5 = (lit(r.get(c)) for c in ["KeyFld_1_V", "KeyFld_2_V", "KeyFld_3_V", "KeyFld_4_V", "KeyFld_5_V"])
        rows.append(
            "INSERT INTO TCD2 "
            '("AbsId","Tcd1Id","DispOrder","KeyFld_1_V","KeyFld_2_V","KeyFld_3_V","KeyFld_4_V","KeyFld_5_V") '
            f"VALUES ({absid},{tcd1},{disp},{v1},{v2},{v3},{v4},{v5});"
        )
    out = saida_camada(cfg, "TCD2") / "TCD2_INSERT.sql"
    header = [
        f"-- TCD2 projeto={nome}. skip={sorted(skip) or '-'}.",
        "-- Slot vazio = NULL. Nao usar 0. Definicao → Atualizar depois do INSERT.",
        f"-- Esperado COUNT = {len(rows)}",
        "",
    ]
    out.write_text("\n".join(header + rows + ["", "COMMIT;", ""]), encoding="utf-8")
    print(nome, "TCD2", len(rows), "->", out)


if __name__ == "__main__":
    main()
