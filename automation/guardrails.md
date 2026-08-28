# Guardrails

## Confirmação humana
- DELETE em TCD* / OBNI / OBPL / OCRD
- INSERT em cadastro mestre
- INSERT TCD3 ou TCD5
- Mapear filial/PN sem o cliente desta carga
- Promover dado de cliente para o mestre (IDs, planilha)
- Commitar/publicar qualquer arquivo deste pacote que cite cliente, base ou carga

## Automático
- Ler esta pasta
- Gerar SELECT de validação
- Escrever history/learnings de **método**
- Rascunhar texto ao cliente (sem inventar de-para)

## Sempre
Uma camada por vez. NULL vazio / EfctTo aberto. OBNI.ID deste SAP. Parar no lookup.
`projeto.nome` obrigatório — e fica no config local, nunca neste repo.

## Antes de qualquer push
Varrer o pacote por nome de cliente, CompanyDB, AbsId, BPLId, CardCode, OBNI.ID, OUSG.ID e totais.
Achou → não sobe.
