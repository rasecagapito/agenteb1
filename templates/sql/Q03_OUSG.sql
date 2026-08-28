-- Q03 | OUSG — ID interno. TCD5.UsageCode = ID, nunca o texto da planilha.
-- Exportar DESTE CompanyDB.
SELECT
  T0."ID"    AS "OUSG_ID",
  T0."Usage" AS "Utilizacao"
FROM OUSG T0
ORDER BY T0."ID"
