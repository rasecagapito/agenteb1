# Changelog

Formato: [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/). Versionamento adaptado ao método:

- **MAJOR** — doutrina ou estrutura muda; regra que invalida carga feita na versão anterior.
- **MINOR** — método, query de validação, lookup ou script novo.
- **PATCH** — correção de texto, exemplo ou bug de gerador, sem mudar método.

Toda carga registra em que versão rodou (`projeto.mestre_versao`). Não trocar de versão no meio de uma carga.

## [Não publicado]

## [1.1.0] — 2026-08-28

### Corrigido
- `gerar_tcd3.py` ignorava `skip_prioridades`: a TCD2 filtrava e renumerava, a TCD3 lia o
  arquivo cru e emitia `Tcd2Id` para AbsId que nunca entrou na TCD2. Quebrava só no Q27,
  depois do INSERT. TCD2 e TCD3 passam a ler a grade pelo mesmo `lib_tcd.ler_grade_tcd2`,
  que concentra filtro, ordenação e numeração.

### Adicionado
- TCD3 de produção: vigências das colunas `EfctFrom`/`EfctTo` da grade TCD2. `EfctTo` vazio
  ou `2099-12-31` vira `NULL`; data faltando ou período invertido interrompe a geração em vez
  de gerar parcial. Limitação declarada: uma vigência por combinação (1:1 TCD2→TCD3).
- `hana.batch_size` vale para TCD2, TCD3 e TCD5 — as três já saem fatiadas.
  `tcd5.batch_size` continua aceito como legado.
- `tests/` com 10 casos em `unittest` (sem dependência nova): alinhamento TCD2/TCD3 sob skip,
  produção da TCD3, `NULL` em slot vazio, fatiamento.
- Contrato das grades de entrada documentado em `scripts/README.md`.
- Learning `grade-unica.md`.

### Em aberto
- Montar `TCD2_CARGA.xlsx` / `TCD5_CARGA.xlsx` a partir da planilha fiscal continua manual.
  Automatizar exigiria fixar o formato da planilha sem ter uma em mãos.

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
