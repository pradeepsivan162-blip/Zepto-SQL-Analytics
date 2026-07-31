-- ==========================================
-- Zepto SQL Data Analytics Project
-- File: 04_Business_Analysis.sql
-- Author: S. Pradeep
-- ==========================================

-- 1. Top 10 Best-Value Products Based on Discount Percentage
SELECT DISTINCT
    name,
    category,
    mrp,
    discountPercent
FROM zepto
ORDER BY discountPercent DESC
LIMIT 10;


-- 2. Products with High MRP but Out of Stock
SELECT
    name,
    category,
    mrp,
    outOfStock
FROM zepto
WHERE outOfStock = TRUE
ORDER BY mrp DESC;


-- 3. Estimated Revenue for Each Category
SELECT
    category,
    SUM((mrp - (mrp * discountPercent / 100)) * availableQuantity) AS estimatedRevenue
FROM zepto
GROUP BY category
ORDER BY estimatedRevenue DESC;


-- 4. Products with MRP Greater Than ₹500 and Discount Less Than 10%
SELECT
    name,
    category,
    mrp,
    discountPercent
FROM zepto
WHERE mrp > 500
AND discountPercent < 10;


-- 5. Top 5 Categories Offering the Highest Average Discount
SELECT
    category,
    AVG(discountPercent) AS averageDiscount
FROM zepto
GROUP BY category
ORDER BY averageDiscount DESC
LIMIT 5;


-- 6. Price Per Gram for Products Above 100g
SELECT
    name,
    category,
    mrp,
    weightInGms,
    ROUND(mrp / weightInGms, 2) AS pricePerGram
FROM zepto
WHERE weightInGms > 100
ORDER BY pricePerGram ASC;


-- 7. Categorize Products by Weight
SELECT
    name,
    category,
    weightInGms,
    CASE
        WHEN weightInGms < 250 THEN 'Low'
        WHEN weightInGms BETWEEN 250 AND 1000 THEN 'Medium'
        ELSE 'Bulk'
    END AS ProductSize
FROM zepto;


-- 8. Total Inventory Weight Per Category
SELECT
    category,
    SUM(weightInGms * availableQuantity) AS totalInventoryWeight
FROM zepto
GROUP BY category
ORDER BY totalInventoryWeight DESC;