# Changelog

Formato: [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/). Versionamento adaptado ao método:

- **MAJOR** — doutrina ou estrutura muda; regra que invalida carga feita na versão anterior.
- **MINOR** — método, query de validação, lookup ou script novo.
- **PATCH** — correção de texto, exemplo ou bug de gerador, sem mudar método.

Toda carga registra em que versão rodou (`projeto.mestre_versao`). Não trocar de versão no meio de uma carga.

## [Não publicado]

## [1.0.0] — 2026-08-27

### Adicionado
- Cérebro multi-harness `AGENTS.md` + ponteiros Claude/Gemini/Cursor e `providers/registry.md`.
- Módulos `context/`: produto, arquitetura, carga-tcd, lookups, formatação, validação, evolução, stack.
- Workers: carga-sap, consultor, documentador.
- Procedures: carga, status, wrapup, handoff, evoluir.
- Geradores `scripts/`: TCD2, TCD3 (modo teste), TCD5 com bloqueio por OUSG ausente, fatiador de lotes.
- Templates SQL: extração (Q01–Q04, Q_OBNI) e validação (Q22, Q27, Q29, Q30) + limpeza TCD3/TCD5.
- Learnings de método: ordem de camadas, 80401-9, OBNI, OUSG, NULLs, lotes HANA, teste vs produção, TaxCode de compra, identidade funcional.
- Versionamento: `VERSION`, este changelog, `projeto.mestre_versao` no config e pin de tag por carga.
- `templates/projeto/` — esqueleto do repositório de carga (onde o dado do cliente fica).

### Regra de privacidade
- Nenhum arquivo deste repo nomeia cliente, base ou carga (`AGENTS.md` regra 11).
- Pasta de casos por cliente não existe. Lição sobe anônima ou não sobe.
