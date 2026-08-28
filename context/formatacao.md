# Formatação

- TCD2 KeyFld vazio → SQL `NULL`. Nunca `0` nem `'0'` (0 é valor válido de alguns combos; vazio não é 0).
- TCD3 `EfctTo` aberto → `NULL`. Nunca `2099-12-31` nem `9999-12-31`.
- TCD3.TaxCode no tipo MI → `NULL`.
- Números vindos do Excel como `12.0` → gravar `12` se for ID.
- Filial: gravar BPLId inteiro em string (`"3"`), não o nome da filial, salvo a TCD1 deste SAP pedir outra coisa.
- INSERT: aspas simples no SQL; `'` no texto vira `''`.
- Identificar regra para o fiscal: Prioridade + chaves + utilização. Não AbsId do arquivo (a tela pode renumerar depois de Atualizar).
