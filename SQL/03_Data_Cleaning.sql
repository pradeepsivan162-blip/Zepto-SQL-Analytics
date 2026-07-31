-- ==========================================
-- Zepto SQL Data Analytics Project
-- File: 03_Data_Cleaning.sql
-- Author: S. Pradeep
-- ==========================================

-- Find products with invalid prices
SELECT *
FROM zepto
WHERE mrp = 0
   OR discountSellingPrice = 0;

-- Delete products with MRP = 0
DELETE FROM zepto
WHERE mrp = 0;

-- Convert prices from paise to rupees
UPDATE zepto
SET mrp = mrp / 100.0,
    discountSellingPrice = discountSellingPrice / 100.0;

-- Verify updated prices
SELECT
    name,
    mrp,
    discountSellingPrice
FROM zepto
LIMIT 10;