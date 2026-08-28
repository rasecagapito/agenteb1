# Lookups

Mensagem da UI `[Nome da tabela - valor]` ou 80401-9 = o valor não existe no cadastro **deste** CompanyDB.

| Sintoma | Tabela | Valor que a TCD2/TCD5 espera |
|---|---|---|
| Indexador numérico do Brasil | OBNI | `OBNI.ID` (não `Code`). Filtrar IndexType da definição desta empresa |
| Filiais | OBPL | `BPLId` ativo aqui |
| Parceiro | OCRD | `CardCode` deste SAP (fornecedor S se a regra for compra). Código igual noutro SAP pode ser outra empresa |
| Utilização | OUSG | `OUSG.ID` numérico |
| Código imposto | OSTC | `OSTC.Code` |
| Estado | OCST | código UF |
| Grupo itens | OITB | `ItmsGrpCod` |
| UDF | CUFD/UFD1 | valor válido da lista deste campo |

Não usar BPL2.TributType como tipo tributário da TCD2.

Coincidência de CardCode entre bases (mesmo código, outro nome) → **não usar**. Amarrar por CNPJ + função (S/C), com o cliente.

Queries: `templates/sql/Q01` … `Q04`, `Q_OBNI.sql`. Extração desta base; não reaproveitar xlsx de outro `projeto.nome`.
