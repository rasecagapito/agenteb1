# Procedimento: EVOLUIR o mestre

Obrigatório ao encerrar uma carga. Sem isto o pacote não serve ao próximo analista/IA.
Só depois do wrapup — nunca com carga aberta (regra 12).

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

## Publicar versão (obrigatório se algo mudou)
1. Escolher o degrau:
   - **MAJOR** — doutrina/estrutura muda; regra que invalida carga da versão anterior.
   - **MINOR** — método, query, lookup ou script novo.
   - **PATCH** — correção de texto, exemplo ou bug de gerador, sem mudar método.
2. `VERSION` ← novo número. `AGENTS.md` → linha **Fase**.
3. `CHANGELOG.md` → mover de `[Não publicado]` para a nova seção, com data real.
4. Commit, tag e release:
   ```
   git commit -am "feat: <lição>"
   git tag -a vX.Y.Z -m "<resumo>"
   git push && git push --tags
   gh release create vX.Y.Z --notes-from-tag
   ```
5. Sem bump, o próximo analista não sabe que mudou. Mudança sem tag não existe.

## Proibido promover
Nome do cliente (em texto, título de arquivo ou exemplo de config), CompanyDB, AbsId, BPLId, CardCode, OBNI.ID, OUSG.ID, linhas da planilha, totais, senha, `skip_prioridades` como default universal.

## Confirmar ao humano
Lista `+` método promovido / `−` o que ficou retido no repo do projeto. E a versão publicada.
