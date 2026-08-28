# Evolução do mestre (obrigatória)

Este pacote **não é estático**. Cada carga deve devolver método. Sem isso o próximo analista (outra IA, outro cliente) repete o mesmo erro.

## Depois de fechar uma carga
Seguir `automation/procedures/evoluir.md`.

Promover para `context/` ou `memory/learnings/` quando:
- 80401-9 apontar tabela ainda não listada
- HANA recusar tamanho/lote diferente de 500
- Nova regra de NULL, OBNI, OUSG, TCD3 teste vs produção
- Query de validação que passou a ser necessária
- Harness novo (como essa IA lê o cérebro)

Não promover:
- Nome do cliente, `projeto.nome`, CompanyDB, planilha
- AbsId, BPLId, CardCode, OBNI.ID, OUSG.ID, totais daquela carga
- skip de uma prioridade específica como se fosse lei universal
- Textos de utilização de um cliente

## Onde gravar
- Dados, SQL e history da carga: repositório **do projeto**, fora deste pacote.
- Neste pacote, só a lição técnica: `memory/learnings/{tema}.md`, escrita como regra geral.
- Handoff do mestre: `memory/handoff.md` (sem nome de cliente).

## Privacidade
Este repo é público-por-suposição. Nenhum arquivo daqui identifica cliente, carga ou base.
Não existe pasta de casos por cliente. A lição sobe anônima ou não sobe.
