SELECT
name,
category,
mrp,
RANK() OVER
(
ORDER BY mrp DESC
)
AS PriceRank
FROM zepto;