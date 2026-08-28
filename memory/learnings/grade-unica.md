# Uma grade, todas as camadas

TCD2 e TCD3 têm de ler a **mesma** grade, pela mesma função, com o mesmo filtro.

Se a TCD2 aplica `skip_prioridades` e renumera, e a TCD3 lê o arquivo cru, os
`Tcd2Id` da TCD3 apontam para AbsId que nunca entrou na TCD2. Nada falha na
geração: o erro só aparece no Q27 (`abertos = COUNT TCD2`), depois do INSERT
no HANA — e parece problema de carga, não de script.

Regra: filtro e numeração ficam num único leitor (`lib_tcd.ler_grade_tcd2`).
Camada nova lê por ele. Contrato: linha *i* pós-filtro ⇒ `AbsId = i`.
