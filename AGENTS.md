# Agente: mestre-impostos
> Cérebro canônico. Todas as IAs (Claude, Codex, GPT, Gemini, DeepSeek, Cursor, Kimi, GLM) leem isto.
> Detalhe em `context/`. Estado vivo em `memory/handoff.md`. ≤ 150 linhas.

## Protocolo de Arranque (qualquer IA)
1. Ler `memory/handoff.md`.
2. Ler `context/carga-tcd.md` e `context/evolucao.md`.
3. Exigir **nome do projeto** (`projeto.nome`) e **versão do mestre** (`projeto.mestre_versao` = tag em que esta carga roda; ver `VERSION`). Sem nome → parar. Não assumir cliente anterior.
4. Carregar só o `context/` da tarefa. Não copiar AbsId, BPLId, CardCode, OBNI.ID, OUSG.ID de outro projeto.

## Identidade
- **Pacote**: método de carga de determinação de imposto SAP B1 (HANA), tipo MI
- **Não é**: um CompanyDB, uma planilha, nem a carga de um cliente específico
- **Uso**: copiar/anexar esta pasta; preencher `config.yaml` com o nome deste cliente/carga

## Módulos
- @context/produto.md
- @context/arquitetura.md
- @context/carga-tcd.md
- @context/lookups.md
- @context/formatacao.md
- @context/validacao.md
- @context/evolucao.md
- @context/stack.md

## Workers
- **Carga SAP** (@workers/carga-sap.md) — gerar/validar TCD por camada
- **Consultor** (@workers/consultor.md) — bloqueio em linguagem da planilha
- **Documentador** (@workers/documentador.md) — history + promover learning ao mestre

## Regras (todas as cargas)
1. Uma camada por vez: TCD1 tela → TCD2 → TCD3 → TCD5. TCD4 é withholding (WT), fora do MI.
2. INSERT no HANA Studio. SELECT no gerador B1. Depois: Definicao → Atualizar.
3. Slot TCD2 vazio = `NULL`, nunca `0`. `EfctTo` aberto = `NULL`, nunca `2099-12-31`.
4. Tipo tributário na TCD2 = `OBNI.ID` do IndexType **desta** empresa (descobrir). Não BPL2.TributType.
5. TCD5.UsageCode = `OUSG.ID` numérico desta base. Sem cadastro → bloquear. Não inventar.
6. TCD3.TaxCode no MI = `NULL` (código na TCD5).
7. `[Tabela - valor]` / 80401-9 = cadastro inexistente. Parar. Pedir de-para.
8. AbsId não viaja entre CompanyDB nem entre projetos. Identidade = prioridade + chaves + uso + datas.
9. Script HANA grande: lotes de 500 INSERT. Relançar TCD5 só depois de limpar residual (unique AbsId).
10. Depois de cada projeto: `automation/procedures/evoluir.md` — método sobe ao mestre; dados do cliente não.
11. Privacidade: nenhum arquivo deste repo nomeia cliente, base ou carga. Nome vive só em `config.yaml` (não versionado) e no repo do projeto. Lição sobe anônima ou não sobe.
12. Versão: uma carga roda numa tag fixa do mestre (`VERSION` + `projeto.mestre_versao`). Não atualizar o método no meio da carga — invalida validação já rodada. Evoluir só depois do wrapup.

## Ciclo
| Intenção | Claude | Todas as IAs |
|---|---|---|
| Carga | `/carga` | `automation/procedures/carga.md` |
| Estado | `/status` | `automation/procedures/status.md` |
| Wrapup | `/wrapup` | `automation/procedures/wrapup.md` |
| Evoluir mestre | `/evoluir` | `automation/procedures/evoluir.md` |

## Config
`config.example.yaml` → copiar para `config.yaml` (ou para o repo do cliente).
Campos obrigatórios: `projeto.nome` e `projeto.mestre_versao`. Totais, OBNI, OUSG, skips e datas saem **daquele** SAP e daquela planilha.

## Estado
- **Fase**: mestre v1.1.0 (ver `VERSION` / `CHANGELOG.md`) — geradores com testes; TCD3 de produção disponível; montagem das grades ainda manual
- Dinâmico: `memory/handoff.md`
