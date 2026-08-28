# Procedimento: CARGA TCD

Provider-neutro. Claude: `/carga`. Outras IAs: "faz a carga do projeto NOME".

## 0. Identidade e versão
- `projeto.nome` informado pelo humano ou em `config.yaml`. Vazio → parar.
- Não carregar config de outro nome.
- Pinar o mestre na tag desta carga: `git checkout v{X.Y.Z}` (última tag, salvo combinação em contrário). Gravar em `projeto.mestre_versao`.
- Daí até o wrapup, não atualizar o mestre. Método novo no meio da carga invalida validação já rodada.

## 1. TCD1
- Tela Definição. Rodar `templates/sql/Q02_TCD1.sql`.
- Preencher `tcd1` + `chaves_por_prioridade` no config deste projeto.

## 2. Mestres
- OBNI (IndexType desta definição), OUSG, OSTC, e os lookups das chaves usadas (OBPL, OCRD, OCST, OITB, UFD1).
- Exportar para o repo **deste** projeto. Não usar extração de outro cliente.

## 3. TCD2
- `python scripts/gerar_tcd2.py --config config.yaml`
- INSERT HANA. Definicao → Atualizar.
- Se 80401-9: parar, cadastro ou skip da **aquela** prioridade neste config. Reimportar TCD2 sem apagar TCD1/OBNI certos.
- Validar Q22 com os totais gerados.

## 4. TCD3
- Só depois da UI TCD2 gravar.
- Teste ou produção conforme `tcd3.modo_teste` combinado com o cliente deste projeto.
- INSERT. Atualizar. Q27.

## 5. TCD5
- Gerar. Fatiar (`batch_size`). Se unique AbsId: limpar TCD5 desta determinação e relançar.
- Q29 + Q30. Atualizar. Teste na tela (gravar uma regra nova, se o analista puder).

## 6. Fechar
- Wrapup no repo do cliente.
- Evoluir o mestre (`procedures/evoluir.md`).
