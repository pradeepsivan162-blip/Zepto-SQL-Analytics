# Collection of pre-built SQL business queries for Zepto SQL Analytics

PREBUILT_QUERIES = {
    "Total Summary Stats": """SELECT 
    COUNT(*) AS total_products,
    COUNT(DISTINCT category) AS total_categories,
    SUM(mrp) AS total_mrp,
    SUM(quantity) AS total_quantity,
    ROUND(AVG(discountPercent), 2) AS avg_discount_percent
FROM zepto;""",

    "Top 10 Best-Value Products (Highest Discount)": """SELECT DISTINCT
    name,
    category,
    mrp,
    discountPercent
FROM zepto
ORDER BY discountPercent DESC
LIMIT 10;""",

    "Out of Stock Products with High MRP": """SELECT
    name,
    category,
    mrp,
    outOfStock
FROM zepto
WHERE outOfStock = TRUE
ORDER BY mrp DESC;""",

    "Estimated Revenue by Category": """SELECT
    category,
    ROUND(SUM((mrp - (mrp * discountPercent / 100)) * availableQuantity), 2) AS estimatedRevenue
FROM zepto
GROUP BY category
ORDER BY estimatedRevenue DESC;""",

    "High MRP (> 500) & Low Discount (< 10%)": """SELECT
    name,
    category,
    mrp,
    discountPercent
FROM zepto
WHERE mrp > 500
AND discountPercent < 10;""",

    "Top 5 Categories by Highest Avg Discount": """SELECT
    category,
    ROUND(AVG(discountPercent), 2) AS averageDiscount
FROM zepto
GROUP BY category
ORDER BY averageDiscount DESC
LIMIT 5;""",

    "Price Per Gram for Products > 100g": """SELECT
    name,
    category,
    mrp,
    weightInGms,
    ROUND(mrp / weightInGms, 2) AS pricePerGram
FROM zepto
WHERE weightInGms > 100
ORDER BY pricePerGram ASC;""",

    "Categorize Products by Weight (Low / Medium / Bulk)": """SELECT
    name,
    category,
    weightInGms,
    CASE
        WHEN weightInGms < 250 THEN 'Low'
        WHEN weightInGms BETWEEN 250 AND 1000 THEN 'Medium'
        ELSE 'Bulk'
    END AS ProductSize
FROM zepto;""",

    "Total Inventory Weight per Category": """SELECT
    category,
    SUM(weightInGms * availableQuantity) AS totalInventoryWeight
FROM zepto
GROUP BY category
ORDER BY totalInventoryWeight DESC;""",

    "Price Rank using Window Function": """SELECT
    name,
    category,
    mrp,
    RANK() OVER (ORDER BY mrp DESC) AS PriceRank
FROM zepto;""",

    "Highest Discounted Product per Category (CTE + Window Fn)": """WITH RankedProducts AS (
    SELECT *,
    ROW_NUMBER() OVER (
        PARTITION BY category
        ORDER BY discountPercent DESC
    ) AS rn
    FROM zepto
)
SELECT category, name, mrp, discountPercent
FROM RankedProducts
WHERE rn = 1
ORDER BY discountPercent DESC;"""
}
