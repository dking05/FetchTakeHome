#### What is the percentage of sales in the Health & Wellness category by generation?

WITH user_generations AS (
    SELECT 
        id AS user_id,
        birth_date,
        CASE 
            WHEN birth_date BETWEEN '1928-01-01' AND '1945-12-31' THEN 'Silent Generation'
            WHEN birth_date BETWEEN '1946-01-01' AND '1964-12-31' THEN 'Baby Boomers'
            WHEN birth_date BETWEEN '1965-01-01' AND '1980-12-31' THEN 'Gen X'
            WHEN birth_date BETWEEN '1981-01-01' AND '1996-12-31' THEN 'Millennials'
            WHEN birth_date BETWEEN '1997-01-01' AND '2012-12-31' THEN 'Gen Z'
            ELSE 'Unknown' 
        END AS generation
    FROM users
),

category_sales AS (
    SELECT 
        t.user_id,
        p.category_1,
        t.final_sale
    FROM transactions t
    JOIN products p ON t.barcode = p.barcode
    WHERE p.category_1 = 'Health & Wellness'
),

sales_by_generation AS (
    SELECT 
        ug.generation,
        SUM(cs.final_sale) AS total_sales
    FROM category_sales cs
    JOIN user_generations ug ON cs.user_id = ug.user_id
    GROUP BY ug.generation
),

total_sales AS (
    SELECT SUM(total_sales) AS total FROM sales_by_generation
)

SELECT 
    s.generation,
    s.total_sales,
    ROUND((s.total_sales / t.total) * 100, 2) AS percentage_of_total_sales
FROM sales_by_generation s, total_sales t
ORDER BY s.total_sales DESC;

#### What are the top 5 brands by sales among users that have had their account for at least six months?

WITH eligible_users AS (
    SELECT 
        id AS user_id
    FROM users
    WHERE created_date <= CURRENT_DATE - INTERVAL '6 months'
),

brand_sales AS (
    SELECT 
        p.brand,
        SUM(t.final_sale) AS total_sales
    FROM transactions t
    JOIN products p ON t.barcode = p.barcode
    JOIN eligible_users u ON t.user_id = u.user_id
    GROUP BY p.brand
)

SELECT 
    brand, 
    total_sales
FROM brand_sales
ORDER BY total_sales DESC
LIMIT 5;

#### Which is the leading brand in the Dips & Salsa category?

WITH category_sales AS (
    SELECT 
        p.brand,
        SUM(t.final_sale) AS total_sales
    FROM transactions t
    JOIN  products p ON t.barcode = p.barcode
    WHERE  p.category_2 = 'Dips & Salsa'
    GROUP BY p.brand
)
SELECT 
    brand,
    total_sales
FROM category_sales
ORDER BY total_sales DESC
LIMIT 1;
