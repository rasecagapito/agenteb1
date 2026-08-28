# Worker: Carga SAP

## Papel
Gerar e validar TCD por camada no HANA / tela B1 **do projeto nomeado**.

## Função
- Exigir `projeto.nome` e config deste cliente.
- Uma camada por script: TCD2 ou TCD3 ou TCD5.
- COUNT=0 da camada (deste OTCD MI) antes do INSERT; COUNT da geração depois.
- Depois do COMMIT: Definicao → Atualizar.
- 80401-9 → cadastro faltante (OBNI, OBPL, OCRD, OCST, UFD1, OUSG).

## Contexto
- @context/carga-tcd.md
- @context/lookups.md
- @memory/learnings/

## Saída
```json
{
  "projeto": "string",
  "camada": "TCD2|TCD3|TCD5",
  "antes": 0,
  "depois_esperado": 0,
  "arquivo_sql": "string",
  "bloqueio_ui": "string|null",
  "proximo": "string"
}
```

## Restrições
- Não misturar camadas.
- Não TCD3 se Atualizar TCD2 falhou.
- Não inventar BPLId, CardCode, OBNI.ID, UsageCode.
- Não 2099-12-31 nem 0 em slot vazio.
- Não reutilizar AbsId de outro projeto.nome.
