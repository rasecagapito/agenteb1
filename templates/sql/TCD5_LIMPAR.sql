-- Limpar TCD5 da determinação MI deste CompanyDB antes de relançar (unique AbsId)
DELETE FROM TCD5
WHERE "TcdId" IN (SELECT T0."AbsId" FROM OTCD T0 WHERE T0."TcdType" = 'MI')
