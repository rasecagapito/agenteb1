# HANA lotes

Console recusa script grande (*SQL console content is too large* / 257).
~700 INSERT costuma passar; milhares não. Fatia 500 (`tcd5.batch_size`).
Unique constraint AbsId = residual. Limpar TCD5 desta determinação antes de relançar. Não pular AbsId.
Gerador B1 não executa INSERT.
