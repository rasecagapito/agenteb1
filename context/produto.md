# Produto

## Purpose
Carregar determinação de código de imposto (SAP B1 Brasil, HANA, tipo MI) a partir da planilha **deste** projeto, com SQL gerado e validação na tela.

## O que é um projeto
Um projeto = um nome + um CompanyDB + uma planilha + os mestres **daquele** SAP.
O pacote `mestre-impostos` não tem cliente embutido. Um cliente só entra via `projeto.nome`, no config local, que não é versionado.

## Público
- Fiscal: linguagem da planilha (prioridade, chaves, utilização, código).
- Analista Seidor: HANA, TCD, 80401-9, de-para.

## Fora
- TCD4 / withholding.
- Inventar filial, PN, OBNI, OUSG, código de imposto.
- Replicar AbsId de um CompanyDB em outro, ou de um projeto em outro.
