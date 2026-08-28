# Validação

Gerador B1: **uma** SELECT (UNION ALL). Não executa INSERT.

Padrão da grade: Grupo, Check, Valor, Esperado, Resultado (OK/FALHOU).

| Camada | Template | Esperados |
|---|---|---|
| TCD2 | `templates/sql/Q22_TCD2_validar.sql` | COUNT e por prioridade = geração **deste** projeto |
| TCD3 | `templates/sql/Q27_TCD3_validar.sql` | geradores preenchem totais; teste e produção 1:1 = 1 aberto por TCD2; N vigências = total > COUNT TCD2 e abertos = COUNT TCD2 |
| TCD5 | `templates/sql/Q29_TCD5_validar.sql` | total TCD5; TCD3 cobertas; prio skip = 0; OUSG/OSTC = 0 órfãos |
| TCD5 venda vazia | `templates/sql/Q30_TCD5_taxcode_vazio.sql` | listar; se PurTaxCode preenchido e uso de entrada, aceitar até o fiscal dizer o contrário |

Q27 `TaxCode_preenchido > 0` no MI: residual de teste na tela, não da geração TCD3 (que manda NULL). Zerar TaxCode TCD3 e Atualizar.

Não colar esperados de outro `projeto.nome`.
