-- OBNI — tipo tributário. Descobrir IndexType DESTA definição (não assumir 18).
-- TCD2 grava OBNI.ID, não OBNI.Code, não BPL2.TributType.
SELECT
  CAST(T0."ID" AS NVARCHAR(20))        AS "ID_para_TCD2",
  CAST(T0."Code" AS NVARCHAR(20))      AS "Codigo",
  CAST(T0."IndexType" AS NVARCHAR(10)) AS "IndexType",
  CAST(T0."Descr" AS NVARCHAR(254))    AS "Descricao"
FROM OBNI T0
ORDER BY T0."IndexType", T0."ID"
