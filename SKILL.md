---
name: mestre-impostos
description: >-
  Carga de determinação de imposto SAP Business One Brasil (HANA), tipo MI
  (OTCD/TCD1/TCD2/TCD3/TCD5). Usa quando o analista for carregar determinação,
  gerar INSERT TCD, validar Q27/Q29, tratar 80401-9, OBNI, OUSG, lotes HANA,
  ou iniciar um projeto novo de impostos. Cada cliente é um projeto.nome;
  não reutilizar AbsId/BPLId/CardCode de outra carga.
---

# mestre-impostos

Ler `AGENTS.md` e seguir `automation/procedures/carga.md`.

## Obrigatório no arranque
1. Nome do projeto (`config.yaml` → `projeto.nome`). Sem nome, parar.
2. Não copiar IDs, nomes ou totais de outra carga.
3. Extrair mestres **deste** CompanyDB (OBNI, OUSG, OSTC, TCD1 KeyFld).

## Camadas
TCD1 tela → TCD2 INSERT + Atualizar sem 80401-9 → TCD3 → TCD5.
TCD4 = WT, fora do MI.

## Scripts
- `scripts/gerar_tcd2.py`
- `scripts/gerar_tcd3.py`
- `scripts/gerar_tcd5.py`
- `scripts/fatiar_inserts.py`

## Evolução
Após cada projeto: `automation/procedures/evoluir.md`.
