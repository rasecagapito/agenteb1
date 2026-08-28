# Esqueleto do repositório de carga

Copiar esta pasta para **fora** do mestre e renomear com o nome da carga.
Aqui mora o que **não** pode entrar no mestre-impostos: nome do cliente, CompanyDB, planilha, extrações, AbsId, totais.

```
{NOME_DA_CARGA}/
  config.yaml              ← cópia de config.example.yaml do mestre, preenchida
  planilha/                ← .xlsx de determinação deste cliente
  extracoes/               ← Q01–Q04 e Q_OBNI exportados DESTE CompanyDB
  saida/                   ← gerado pelos scripts: TCD2/ TCD3/ TCD5/
  memory/
    handoff.md             ← estado vivo desta carga
    history/               ← uma sessão por arquivo
  README.md
```

## Montar
1. Copiar esta pasta. `mv gitignore .gitignore`.
2. `cp {mestre}/config.example.yaml config.yaml` e preencher `projeto.nome`.
3. Pinar o mestre: `git -C {mestre} checkout vX.Y.Z` → gravar em `projeto.mestre_versao`.
4. Rodar `automation/procedures/carga.md` do mestre.

## Regras
- Este repo é **privado**. O mestre é público-por-suposição — nada daqui sobe para lá.
- Não trocar a versão do mestre no meio da carga (regra 12).
- Ao fechar: `wrapup` aqui, depois `evoluir` no mestre — só método, anônimo.
