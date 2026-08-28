# Carga TCD — método (válido para qualquer projeto)

Antes de gerar SQL: `projeto.nome` preenchido. Extrair TCD1/OBNI/OUSG/OSTC **deste** CompanyDB.

## TCD1
Cadastrar prioridades na tela Definição. Os números KeyFld (25, 6, 17…) são **desta** definição, não de outro cliente. UDF 17 pode repetir na tupla; o SAP distingue pelo picker.

Query: `templates/sql/Q02_TCD1.sql`. Preencher `tcd1` e `chaves_por_prioridade` no config deste projeto.

## TCD2
Uma linha por combinação de valores das chaves da prioridade. Slot sem valor = `NULL`, nunca `"0"`.
Tipo tributário da empresa = `OBNI.ID` do IndexType descoberto aqui (query `Q_OBNI.sql`). Não gravar BPL2.TributType (11–14 etc.).
Grupo de itens: mapear nome da planilha → `OITB.ItmsGrpCod` **deste** SAP (`mapeamentos.grupo_item`).
Prioridade que o SAP recusar (filial/PN inexistente): colocar em `skip_prioridades` **deste** config. Não pular “a 21” por hábito.

Gerar: `scripts/gerar_tcd2.py`. Validar: `templates/sql/Q22_TCD2_validar.sql` (totais saem da geração).

## TCD3
MI: `TaxCode` fica NULL. Código é TCD5.

- **Teste** (`tcd3.modo_teste: true`): 1 período aberto por TCD2. `EfctFrom` = `tcd3.test_from` combinado com o cliente. `EfctTo` = NULL.
- **Produção 1:1** (`modo_teste: false`): vigências nas colunas `EfctFrom`/`EfctTo` da grade TCD2.
- **Produção N:1** (`TCD3/TCD3_CARGA.xlsx`): várias vigências para a mesma combinação. Tem precedência.

Data faltando, período sobreposto, dois períodos abertos na mesma TCD2 ou TCD2 sem vigência → o gerador para. Não gera parcial: período sobreposto torna a determinação ambígua no SAP.

Nunca gravar `2099-12-31` em `EfctTo`.

## TCD5
`Tcd3Id` aponta para TCD3 deste ambiente. Em teste 1:1, Tcd3Id costuma igualar AbsId TCD2 — só se a TCD3 deste projeto for 1:1.
UsageCode = `OUSG.ID` desta extração. Texto da planilha não entra. Sem match → bloquear linha (aba BLOQUEADOS), não inventar ID.
TaxCode/Exp/Pur devem existir em OSTC desta base. Utilização só de compra pode ter TaxCode (venda) vazio e PurTaxCode preenchido — não tratar como lote falho sem olhar Q30.

HANA: todas as camadas saem fatiadas em `hana.batch_size` (500). Arquivo único grande → *SQL console content is too large* / 257.
Unique constraint em AbsId → limpar TCD5 desta determinação antes de relançar.

## Gate de tela
INSERT HANA não substitui Atualizar. 80401-9 `[Tabela - valor]` = valor inexistente no combo. Corrigir mestre ou de-para; reimportar só a camada quebrada. Não apagar TCD1 nem OBNI já certos.
