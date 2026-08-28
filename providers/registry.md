# Registro de provedores

Cérebro canônico: `AGENTS.md`. Ponteiro nunca duplica regra.

| Provedor | Entrada | Import | Slash | Nota |
|---|---|---|---|---|
| Claude Code | `CLAUDE.md` | `@AGENTS.md` | `.claude/commands/` | |
| Cursor | `AGENTS.md` + `SKILL.md` | nativo | opcional | Skill em `C:\Dev\Skill\mestre-impostos` ou `.cursor/skills/` |
| Codex / GPT CLI | `AGENTS.md` | nativo | não | Pedir em linguagem natural; ler `automation/procedures/` |
| ChatGPT (web) | anexar pasta | — | não | Primeira msg: leia AGENTS.md. Projeto chama-se X |
| Gemini CLI | `GEMINI.md` | `@AGENTS.md` | não | |
| DeepSeek / Kimi / GLM | conforme harness | ⚠️ | não | Se OpenAI-compat → AGENTS.md. Se via Claude base-url → CLAUDE.md |
| OpenCode / Aider | `AGENTS.md` | — | não | |

Novo provedor: descobrir o bootstrap, criar ponteiro `@AGENTS.md` se houver import, senão instruir a ler AGENTS.md. Registrar nesta tabela.

Regra: nunca copiar o cérebro para o arquivo do provedor.
