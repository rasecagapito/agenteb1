# Handoff — estado vivo
> Lê primeiro. Sem projeto.nome → não inventar cliente.

## Sessão
- IA: Claude Opus 5 · Quando: 2026-08-27

## Projeto
- nome: nenhum (mestre entre cargas)
- camada: —

## Narrativa
- Feito: pacote v1.0.0. Privacidade fechada (regra 11, sem casos por cliente). Versionamento: VERSION + CHANGELOG + tag por carga (regra 12). Esqueleto do repo de carga em templates/projeto/.
- Decidido: cada carga roda numa tag fixa (projeto.mestre_versao) e grava history no próprio repo. Só método e lição anônima entram aqui.
- Gotchas: não copiar SQL/AbsId/OBNI entre cargas; não gravar nome de cliente em nenhum arquivo daqui.
- Bloqueio: repo GitHub agenteb1 pendente de deletar/recriar (objetos antigos ainda alcançáveis por SHA). Tag v1.0.0 sobe no recreate.
- Próxima intenção: próxima carga copia templates/projeto/, preenche nome + mestre_versao, segue carga.md.
