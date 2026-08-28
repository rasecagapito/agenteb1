# Vigência é camada, não coluna

TCD3 é 1:N com TCD2: a mesma combinação de chaves pode mudar de código ao longo
do tempo. Modelar vigência como coluna da TCD2 só cobre o caso de uma vigência
por regra.

Validar antes de gerar, nunca depois do INSERT:
- períodos sobrepostos na mesma TCD2 → determinação ambígua, o SAP não sabe qual aplicar;
- mais de um período aberto (`EfctTo` NULL) na mesma TCD2 → mesmo problema;
- TCD2 sem nenhuma TCD3 → regra inserida que nunca determina nada.

Buraco entre períodos é legítimo (a regra simplesmente não vale naquele intervalo).

AbsId da TCD3 é sequência própria, não herda o da TCD2 quando há N vigências.
Quem monta a camada seguinte referencia a grade exportada, não a linha da planilha.
