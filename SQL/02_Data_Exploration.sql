SELECT COUNT(*) FROM zepto;

SELECT *
FROM zepto
LIMIT 10;

SELECT DISTINCT category
FROM zepto;

SELECT *
FROM zepto
WHERE name IS NULL
OR category IS NULL
OR mrp IS NULL
OR discountPercent IS NULL
OR availableQuantity IS NULL
OR weightInGms IS NULL
OR outOfStock IS NULL
OR quantity IS NULL;

SELECT outOfStock,
COUNT(*)
FROM zepto
GROUP BY outOfStock;