# Scripts

Dependem de `config.yaml` com `projeto.nome`. Saída: `saida/{nome}/TCD2|TCD3|TCD5/`.

```
pip install pandas openpyxl pyyaml
python scripts/gerar_tcd2.py --config caminho/config.yaml
python scripts/gerar_tcd3.py --config caminho/config.yaml
python scripts/gerar_tcd5.py --config caminho/config.yaml
python scripts/fatiar_inserts.py --arquivo saida/NOME/TCD5/TCD5_INSERT.sql --lote 500
```

TCD2, TCD3 e TCD5 já saem fatiados em `hana.batch_size` (`_p01.sql`, `_p02.sql`…).
`fatiar_inserts.py` só é necessário para arquivo montado à mão.

## Grades de entrada

Montadas por você a partir da planilha desta carga (não copiar de outro nome).
Ficam em `saida/{nome}/`, junto do que é gerado.

### `TCD2/TCD2_CARGA.xlsx`

| Coluna | Obrigatória | Nota |
|---|---|---|
| `Prioridade` | se houver `skip_prioridades` | usada no filtro e na ordenação |
| `AbsId_TCD1` | sim | AbsId da TCD1 **deste** CompanyDB (Q02) |
| `DispOrder` | não | ausente = ordem da linha |
| `KeyFld_1_V`..`KeyFld_5_V` | sim (podem ser vazias) | vazio → `NULL`, nunca `0` |
| `EfctFrom` | só em TCD3 de produção | data da planilha desta carga |
| `EfctTo` | não | vazio ou `2099-12-31` → `NULL` (aberto) |

**Contrato de identidade**: depois de aplicar `skip_prioridades` e ordenar, a linha *i*
(1-based) vira `TCD2.AbsId = i` e `TCD3.Tcd2Id = i`. Os dois geradores leem a grade
pela mesma função (`lib_tcd.ler_grade_tcd2`) justamente para não divergirem.

### `TCD3/TCD3_CARGA.xlsx` — opcional, para várias vigências na mesma regra

Só é necessário quando uma combinação de chaves muda de código ao longo do tempo
(N vigências por TCD2). Se o arquivo existe, ele manda — `modo_teste` e as colunas
de data da grade TCD2 são ignoradas.

| Coluna | Obrigatória | Nota |
|---|---|---|
| `AbsId_TCD2` | sim | AbsId de `TCD2_GRADE.xlsx`, não a linha da planilha |
| `EfctFrom` | sim | início da vigência |
| `EfctTo` | não | vazio ou `2099-12-31` → aberto |

Recusa a gerar quando: `AbsId_TCD2` não existe na grade (prioridade skipada, por
exemplo), períodos se sobrepõem na mesma TCD2, há mais de um período aberto na
mesma TCD2, ou alguma TCD2 fica sem nenhuma vigência.

### `TCD5/TCD5_CARGA.xlsx`

`AbsId_TCD3`, `UsageCode` **ou** `Usage_texto`, `TaxCode`, `ExpTaxCode`, `PurTaxCode`.
Sem match em OUSG a linha vai para `BLOQUEADOS.xlsx` — não se inventa ID.

OUSG: exportar `templates/sql/Q03_OUSG.sql` neste CompanyDB → `ousg.extracao`.

## Grades exportadas

Cada gerador grava a grade que realmente usou, já filtrada e numerada:

- `TCD2/TCD2_GRADE.xlsx` — base para montar `TCD3_CARGA.xlsx`
- `TCD3/TCD3_GRADE.xlsx` — base para montar `TCD5_CARGA.xlsx` (`AbsId_TCD3`)

Os AbsId nascem da numeração pós-skip: não estão no arquivo de entrada e não devem
ser adivinhados.

## TCD3: teste e produção

- `tcd3.modo_teste: true` — um período aberto por TCD2, a partir de `tcd3.test_from`.
- `tcd3.modo_teste: false` — uma vigência por linha da grade, lendo `EfctFrom`/`EfctTo`.
  Data faltando ou `EfctTo` anterior a `EfctFrom` → para, sem gerar parcial.

Para várias vigências na mesma combinação, monte `TCD3_CARGA.xlsx` (acima) — ele
tem precedência sobre os dois modos.

## Testes

Só stdlib + as dependências acima:

```
python -m unittest discover -s tests -v
```

Cobrem o alinhamento TCD2/TCD3 sob `skip_prioridades`, a produção da TCD3,
`NULL` em slot vazio e o fatiamento por `batch_size`.
