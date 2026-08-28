# -*- coding: utf-8 -*-
"""TCD3: teste = 1 período aberto; produção = datas da planilha deste projeto."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib_tcd import arg_config, load_config, require_projeto, saida_camada, sql_str, to_date

import pandas as pd


def main():
    cfg = load_config(arg_config())
    nome = require_projeto(cfg)
    t3 = cfg.get("tcd3") or {}
    modo = bool(t3.get("modo_teste", True))
    src = saida_camada(cfg, "TCD2") / "TCD2_CARGA.xlsx"
    if not src.exists():
        raise SystemExit(f"Falta {src}")
    df = pd.read_excel(src, sheet_name=0)
    n = len(df)
    otcd = (cfg.get("otcd") or {}).get("abs_id")
    if not otcd:
        raise SystemExit("otcd.abs_id obrigatório (Q01 neste CompanyDB). Não assumir 1.")
    otcd = int(otcd)
    out_dir = saida_camada(cfg, "TCD3")
    rows = []
    if modo:
        test_from = to_date(t3.get("test_from"))
        if test_from is None:
            raise SystemExit(
                "tcd3.test_from obrigatório neste projeto (combinar data com o cliente). "
                "Não copiar data de outro nome."
            )
        for i in range(1, n + 1):
            rows.append(
                "INSERT INTO TCD3 "
                '("AbsId","TcdId","Tcd2Id","EfctFrom","EfctTo","TaxCode") '
                f"VALUES ({i},{otcd},{i},{sql_str(test_from.isoformat())},NULL,NULL);"
            )
        note = f"TESTE 1 periodo aberto {test_from.isoformat()} EfctTo=NULL TaxCode=NULL"
    else:
        raise SystemExit(
            "Produção: gere TCD3 a partir das datas da planilha DESTE projeto "
            "(não copiar períodos de outro nome)."
        )
    header = [
        f"-- TCD3 projeto={nome}. {note}.",
        "-- MI: TaxCode NULL. Nunca EfctTo 2099-12-31.",
        f"-- COUNT esperado = {len(rows)}",
        "",
    ]
    (out_dir / "TCD3_INSERT.sql").write_text(
        "\n".join(header + rows + ["", "COMMIT;", ""]), encoding="utf-8"
    )
    print(nome, "TCD3", len(rows), modo)


if __name__ == "__main__":
    main()
