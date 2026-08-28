-- Q01 | OTCD — AbsId da determinação deste CompanyDB
-- Não assumir AbsId = 1. Filtrar TcdType do config (MI).
SELECT
  T0."AbsId"   AS "AbsId_OTCD",
  T0."TcdType" AS "Tipo"
FROM OTCD T0
ORDER BY T0."AbsId"
