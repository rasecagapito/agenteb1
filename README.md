# mestre-impostos

Método de carga da **determinação de código de imposto** no SAP Business One Brasil (HANA), tipo **MI**.

Esta pasta é o cérebro. Serve para Claude, Codex/GPT, Gemini, DeepSeek, Cursor, Kimi, GLM e qualquer harness que leia arquivos. Não é um plugin de IDE. Não é o cadastro de um cliente.

## Cada carga é um projeto

| Conceito | O que é |
|---|---|
| **Este pacote** | Regras, queries-modelo, geradores, workers |
| **Um projeto** | Um cliente / um CompanyDB / uma planilha. Tem **nome** |

Sem `projeto.nome` a IA **para**. Não herdar CompanyDB, AbsId, OBNI, filial, PN ou totais de outro nome.

```yaml
projeto:
  nome: NOME_DESTE_CLIENTE   # obrigatório e único por carga
  company_db: ""             # preencher depois da extração deste SAP
```

Copie `config.example.yaml` → `config.yaml` (nesta pasta ou no repositório do cliente).

## Como o analista usa (qualquer IA)

1. Entregar esta pasta (clone, zip, ou atalho).
2. Primeira mensagem: *Leia AGENTS.md, memory/handoff.md e context/carga-tcd.md. O projeto chama-se X.*
3. A IA segue `automation/procedures/carga.md`.
4. No fim: wrapup **e** `automation/procedures/evoluir.md` para o mestre crescer (método, não dados do cliente).

### Harness

| Ferramenta | Arquivo de entrada |
|---|---|
| Claude Code | `CLAUDE.md` → `AGENTS.md` |
| Cursor | `AGENTS.md` + `SKILL.md` (ou abrir esta pasta) |
| Codex / GPT CLI | `AGENTS.md` |
| Gemini CLI | `GEMINI.md` → `AGENTS.md` |
| DeepSeek, Kimi, GLM, ChatGPT web | Anexar a pasta; *leia AGENTS.md primeiro* |
| OpenCode / Aider | `AGENTS.md` |

Detalhe: `providers/registry.md`. Slash commands Claude em `.claude/commands/`; nas outras IAs o mesmo texto está em `automation/procedures/`.

## O que este pacote sabe (método)

- Ordem TCD1 (tela) → TCD2 → TCD3 → TCD5. TCD4 = retenção, fora do MI.
- INSERT no HANA Studio; SELECT no gerador B1; Definicao → Atualizar.
- NULL no slot vazio e no `EfctTo` aberto.
- Tipo tributário = `OBNI.ID` do IndexType **desta** empresa (descobrir).
- Uso na TCD5 = `OUSG.ID` desta base.
- 80401-9 = cadastro faltante; não inventar lookup.
- Lotes de 500 INSERT; limpar AbsId antes de relançar.
- Teste: um período aberto por combinação. Produção: datas da planilha daquele projeto.

## O que este pacote não traz

- Planilha fiscal, INSERT com AbsId, lista de filiais/PNs, OBNI de outro SAP.
- Totais (699, 6522, etc.) — saem da geração **deste** projeto.

## Evoluir a cada projeto

O mestre **tem** de melhorar depois de cada cliente. Ver `context/evolucao.md`.

- Sobe: erro novo, query nova, regra de formatação, tamanho de lote.
- Não sobe: nome do cliente, CardCode, BPLId, OBNI.ID, OUSG.ID, planilha, CompanyDB, totais. Nunca, em nenhum arquivo deste repo.

## Scripts

```
pip install pandas openpyxl pyyaml
python scripts/gerar_tcd2.py --config config.yaml
python scripts/gerar_tcd3.py --config config.yaml
python scripts/gerar_tcd5.py --config config.yaml
python scripts/fatiar_inserts.py --arquivo saida/TCD5_INSERT.sql --lote 500
```

Saída em `saida/{projeto.nome}/TCD2|TCD3|TCD5/`.
