-- Q02 | TCD1 — prioridades e KeyFld DESTE SAP (não copiar de outro projeto)
SELECT
  T1."AbsId"    AS "AbsId_TCD1",
  T1."TcdId"    AS "AbsId_OTCD",
  T0."TcdType"  AS "Tipo",
  T1."Priority" AS "Prioridade",
  T1."KeyFld_1",
  T1."KeyFld_2",
  T1."KeyFld_3",
  T1."KeyFld_4",
  T1."KeyFld_5",
  T1."Descr"
FROM TCD1 T1
INNER JOIN OTCD T0 ON T1."TcdId" = T0."AbsId"
WHERE T0."TcdType" = 'MI'
ORDER BY T1."Priority"
