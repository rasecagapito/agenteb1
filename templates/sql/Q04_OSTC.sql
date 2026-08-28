-- Q04 | OSTC — códigos de imposto DESTE CompanyDB
SELECT
  T0."Code"       AS "Codigo",
  T0."Name"       AS "Nome",
  T0."Lock"       AS "Bloqueado",
  T0."ValidForAR" AS "Valido_Venda",
  T0."ValidForAP" AS "Valido_Compra"
FROM OSTC T0
ORDER BY T0."Code"
