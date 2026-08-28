-- Q22 | TCD2 depois do INSERT — totais DESTE projeto (não colar COUNT de outro nome)
SELECT T1."Priority" AS "Prioridade", COUNT(*) AS "Qtd_TCD2"
FROM TCD2 T2
INNER JOIN TCD1 T1 ON T2."Tcd1Id" = T1."AbsId"
INNER JOIN OTCD T0 ON T1."TcdId" = T0."AbsId"
WHERE T0."TcdType" = 'MI'
GROUP BY T1."Priority"
ORDER BY T1."Priority";

SELECT COUNT(*) AS "TCD2_total"
FROM TCD2 T2
INNER JOIN TCD1 T1 ON T2."Tcd1Id" = T1."AbsId"
INNER JOIN OTCD T0 ON T1."TcdId" = T0."AbsId"
WHERE T0."TcdType" = 'MI';
-- Esperado = linhas geradas neste projeto.nome
