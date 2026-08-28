-- Q27 | TCD3 — UMA query. Substituir ESPERADO pelos totais DESTE projeto.
-- Teste: 1 aberto por TCD2, EfctTo NULL, TaxCode NULL, EfctFrom = test_from do config.

SELECT
  CAST('TCD3_total' AS NVARCHAR(40)) AS "Check",
  CAST(COUNT(*) AS NVARCHAR(50)) AS "Valor"
FROM TCD3 T3
INNER JOIN OTCD T0 ON T3."TcdId" = T0."AbsId"
WHERE T0."TcdType" = 'MI'

UNION ALL
SELECT 'TCD3_abertos', CAST(COUNT(*) AS NVARCHAR(50))
FROM TCD3 T3
INNER JOIN OTCD T0 ON T3."TcdId" = T0."AbsId"
WHERE T0."TcdType" = 'MI' AND T3."EfctTo" IS NULL

UNION ALL
SELECT 'TCD3_EfctTo_2099', CAST(COUNT(*) AS NVARCHAR(50))
FROM TCD3 T3
INNER JOIN OTCD T0 ON T3."TcdId" = T0."AbsId"
WHERE T0."TcdType" = 'MI' AND T3."EfctTo" = '2099-12-31'

UNION ALL
SELECT 'TaxCode_preenchido', CAST(COUNT(*) AS NVARCHAR(50))
FROM TCD3 T3
INNER JOIN OTCD T0 ON T3."TcdId" = T0."AbsId"
WHERE T0."TcdType" = 'MI' AND T3."TaxCode" IS NOT NULL

ORDER BY 1
-- Teste: EfctTo_2099=0, TaxCode_preenchido=0, abertos = total = COUNT TCD2 deste projeto
