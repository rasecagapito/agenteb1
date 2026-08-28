# Handoff — estado vivo
> Lê primeiro. Sem projeto.nome → não inventar cliente.

## Sessão
- IA: Claude Opus 5 · Quando: 2026-08-28 18:36

## Projeto
- nome: nenhum (mestre entre cargas)
- camada: —

## Narrativa
- Feito: v1.2.1 — Q27 e validacao.md alinhados a N vigências (o rodapé ainda dizia abertos = total = COUNT TCD2). Antes, v1.2.0: TCD3 com N vigências por TCD2 (TCD3_CARGA.xlsx) e validação de sobreposição; grades numeradas exportadas para a camada seguinte. Antes, v1.1.0: TCD3 alinhada ao filtro da TCD2 (bug que só quebrava no Q27), TCD3 de produção, lotes nas três camadas, tests/ em unittest. Antes: v1.0.0. Privacidade fechada (regra 11, sem casos por cliente). Versionamento: VERSION + CHANGELOG + tag por carga (regra 12). Esqueleto do repo de carga em templates/projeto/.
- Decidido: cada carga roda numa tag fixa (projeto.mestre_versao) e grava history no próprio repo. Só método e lição anônima entram aqui.
- Gotchas: não copiar SQL/AbsId/OBNI entre cargas; não gravar nome de cliente em nenhum arquivo daqui.
- Em aberto: montar TCD2_CARGA/TCD5_CARGA a partir da planilha fiscal continua manual — automatizar exige uma planilha real em mãos (candidato a v1.3.0, com planilha real em mãos).
- Próxima intenção: próxima carga copia templates/projeto/, preenche nome + mestre_versao, segue carga.md.
