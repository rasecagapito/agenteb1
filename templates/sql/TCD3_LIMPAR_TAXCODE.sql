-- MI: zerar TaxCode residual na TCD3 (código fica na TCD5)
UPDATE TCD3
SET "TaxCode" = NULL
WHERE "TaxCode" IS NOT NULL
  AND "TcdId" IN (SELECT T0."AbsId" FROM OTCD T0 WHERE T0."TcdType" = 'MI')
