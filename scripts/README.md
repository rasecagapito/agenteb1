# Scripts

Dependem de `config.yaml` com `projeto.nome`. Saída: `saida/{nome}/TCD2|TCD3|TCD5/`.

```
pip install pandas openpyxl pyyaml
python scripts/gerar_tcd2.py --config caminho/config.yaml
python scripts/gerar_tcd3.py --config caminho/config.yaml
python scripts/gerar_tcd5.py --config caminho/config.yaml
python scripts/fatiar_inserts.py --arquivo saida/NOME/TCD5/TCD5_INSERT.sql --lote 500
```

Arquivos intermediários **deste** projeto (não copiar de outro nome):

- `TCD2/TCD2_CARGA.xlsx` — Prioridade, AbsId_TCD1, DispOrder, KeyFld_1_V..5_V (NULL = vazio)
- `TCD5/TCD5_CARGA.xlsx` — AbsId_TCD3, UsageCode ou Usage_texto, TaxCode, ExpTaxCode, PurTaxCode

OUSG: exportar `templates/sql/Q03_OUSG.sql` neste CompanyDB → `ousg.extracao`.
