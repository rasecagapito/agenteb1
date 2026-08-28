-- Q30 | TCD5 com TaxCode (venda) vazio — listar; não é lote falho se PurTaxCode preenchido
SELECT
  T5."AbsId"      AS "AbsId_TCD5",
  T5."Tcd3Id"     AS "AbsId_TCD3",
  T1."Priority"   AS "Prioridade",
  T5."UsageCode"  AS "OUSG_ID",
  U."Usage"       AS "Utilizacao",
  T5."TaxCode"    AS "Venda",
  T5."ExpTaxCode" AS "Exportacao",
  T5."PurTaxCode" AS "Compra",
  T2."KeyFld_1_V",
  T2."KeyFld_2_V",
  T2."KeyFld_3_V",
  T2."KeyFld_4_V",
  T2."KeyFld_5_V"
FROM TCD5 T5
INNER JOIN TCD3 T3 ON T5."Tcd3Id" = T3."AbsId"
INNER JOIN TCD2 T2 ON T3."Tcd2Id" = T2."AbsId"
INNER JOIN TCD1 T1 ON T2."Tcd1Id" = T1."AbsId"
INNER JOIN OTCD T0 ON T1."TcdId" = T0."AbsId"
LEFT JOIN OUSG U ON U."ID" = T5."UsageCode"
WHERE T0."TcdType" = 'MI'
  AND T5."TaxCode" IS NULL
ORDER BY T5."AbsId"
