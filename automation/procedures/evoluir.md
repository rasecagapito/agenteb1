# Procedimento: EVOLUIR o mestre

Obrigatório ao encerrar uma carga. Sem isto o pacote não serve ao próximo analista/IA.

## O que perguntar
1. Algum 80401-9 / lookup novo?
2. HANA recusou tamanho diferente? Lote mudou?
3. Query de validação nova ou esperados que o template não cobria?
4. Formatação (NULL, datas, UsageCode) que o mestre ainda não diz?
5. Harness que não leu AGENTS.md?

## Aplicar no mestre (`C:\Dev\Skill\mestre-impostos` ou clone)
- Sim a 1–5 → gravar `memory/learnings/{tema}.md` como **regra técnica geral**, sem cliente, sem IDs, sem totais.
- Atualizar `context/` só com regra geral.
- History do mestre: `memory/history/YYYY-MM-DD-HHMM-promocao.md`. Descreve a lição, não a carga.
- Handoff: última promoção. Nunca o nome de quem a originou.

## Proibido promover
Nome do cliente (em texto, título de arquivo ou exemplo de config), CompanyDB, AbsId, BPLId, CardCode, OBNI.ID, OUSG.ID, linhas da planilha, totais, senha, `skip_prioridades` como default universal.

## Confirmar ao humano
Lista `+` método promovido / `−` o que ficou retido no repo do projeto.
