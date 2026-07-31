CREATE VIEW CategorySummary AS

SELECT
category,
COUNT(*) TotalProducts,
AVG(mrp) AveragePrice,
AVG(discountPercent) AverageDiscount
FROM zepto
GROUP BY category;