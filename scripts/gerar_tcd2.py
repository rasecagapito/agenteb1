# -*- coding: utf-8 -*-
"""Gera TCD2 INSERT a partir de TCD2_CARGA.xlsx DESTA carga (não de outro nome)."""
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
    nval,
    require_projeto,
    saida_camada,
    sql_str,
    write_batches,
)

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
    skip = sorted(int(x) for x in (cfg.get("skip_prioridades") or []))
    df = ler_grade_tcd2(cfg)

    rows = []
    for _, r in df.iterrows():
        absid = int(r["AbsId"])
        tcd1 = int(r["AbsId_TCD1"])
        disp = int(r["DispOrder"]) if "DispOrder" in df.columns and not pd.isna(r["DispOrder"]) else absid
        v1, v2, v3, v4, v5 = (
            lit(r.get(c)) for c in ["KeyFld_1_V", "KeyFld_2_V", "KeyFld_3_V", "KeyFld_4_V", "KeyFld_5_V"]
        )
        rows.append(
            "INSERT INTO TCD2 "
            '("AbsId","Tcd1Id","DispOrder","KeyFld_1_V","KeyFld_2_V","KeyFld_3_V","KeyFld_4_V","KeyFld_5_V") '
            f"VALUES ({absid},{tcd1},{disp},{v1},{v2},{v3},{v4},{v5});"
        )

    out = saida_camada(cfg, "TCD2")
    header = [
        f"-- TCD2 carga={nome}. skip={skip or '-'}.",
        "-- Slot vazio = NULL. Nao usar 0. Definicao -> Atualizar depois do INSERT.",
        f"-- Esperado COUNT = {len(rows)}",
        "",
    ]
    write_batches(rows, out, "TCD2_INSERT", batch_size(cfg), header)
    grade = exportar_grade(df, out, "TCD2_GRADE")
    print(nome, "TCD2", len(rows), "->", out)
    print("grade numerada:", grade.name, "— use AbsId dela na TCD3_CARGA")


if __name__ == "__main__":
    main()
