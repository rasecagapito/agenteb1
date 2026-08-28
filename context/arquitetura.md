# Arquitetura

Hierarquia física (todo CompanyDB B1):

```
OTCD (TcdType = MI)
 └── TCD1   prioridade + KeyFld_1..5  (IDs da tela Definição DESTE SAP)
      └── TCD2   combinação KeyFld_1_V..5_V + DispOrder
           └── TCD3   vigência EfctFrom / EfctTo
                └── TCD5   UsageCode + TaxCode / ExpTaxCode / PurTaxCode
```

Joins: `TCD1.TcdId = OTCD.AbsId`; `TCD2.Tcd1Id = TCD1.AbsId`; `TCD3.Tcd2Id = TCD2.AbsId`; `TCD5.Tcd3Id = TCD3.AbsId`.
`TCD5.UsageCode = OUSG.ID`. TCD4 liga em TCD2 e é WT — não usar no fluxo MI.

Identidade entre ambientes: **não** AbsId. Usar tipo + prioridade + valores de chave + EfctFrom + UsageCode.

Ordem de carga: TCD1 na tela → TCD2 INSERT + Atualizar sem 80401-9 → TCD3 → TCD5.
Escrita desta metodologia: INSERT SQL no HANA Studio (combinado com o analista). Gerador B1 só SELECT.
Depois de cada camada: abrir Definição e Atualizar (o INSERT não atualiza o cache da UI).
