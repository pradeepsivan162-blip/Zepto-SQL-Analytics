WITH RankedProducts AS
(
SELECT *,
ROW_NUMBER() OVER
(
PARTITION BY category
ORDER BY discountPercent DESC
) rn
FROM zepto
)

SELECT *
FROM RankedProducts
WHERE rn=1;