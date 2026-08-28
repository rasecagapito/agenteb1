# Procedimento: WRAPUP

1. Hora real (PowerShell `Get-Date -Format 'yyyy-MM-dd HH:mm'`).
2. History no **repo da carga** (esqueleto em `templates/projeto/`): `memory/history/YYYY-MM-DD-HHMM-sessao.md` — projeto.nome, `mestre_versao`, provedor, decisões, COUNT observados, pendências.
3. Handoff da carga: `memory/handoff.md` daquele repo (substituir, não acumular).
4. Learning só se for reutilizável fora desta carga.
5. Se a carga fechou: correr `evoluir.md` no mestre — lição anônima + bump de versão.

Não gravar INSERT/COUNT que não foram observados.
