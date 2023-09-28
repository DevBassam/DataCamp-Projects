--Task1:

SELECT COUNT(info.*) AS total_rows,
       COUNT(description) count_description,
       COUNT(listing_price) AS count_listing_price,
       COUNT(last_visited) AS count_last_visited
FROM info
INNER JOIN finance
USING(product_id) 
INNER JOIN traffic
USING(product_id)

--Task2:

SELECT brand, listing_price::integer, COUNT(finance.*)
FROM brands
INNER JOIN finance
USING(product_id)
WHERE listing_price > 0
GROUP BY brand, listing_price::integer
ORDER BY listing_price DESC

--Task3:

SELECT brand, 
       COUNT(finance.*), 
       SUM(revenue) AS total_revenue,
       CASE WHEN listing_price >= 129 THEN 'Elite'
            WHEN listing_price >= 74 THEN 'Expensive'
            WHEN listing_price >= 42 THEN 'Average'
            ELSE 'Budget' END AS price_category
FROM brands
INNER JOIN finance
USING(product_id)
WHERE brand IS NOT NULL
GROUP BY brand, price_category
ORDER BY total_revenue DESC

--Task4:

SELECT brand, AVG(finance.discount)*100 AS average_discount
FROM brands
INNER JOIN finance
USING(product_id) 
WHERE brand IS NOT NULL
GROUP BY brand

--Task5:

SELECT CORR(reviews,revenue) AS review_revenue_corr
FROM reviews
INNER JOIN finance
USING(product_id)

--Task6:

SELECT TRUNC(LENGTH(description),-2)::numeric AS description_length,
       ROUND(AVG(rating::numeric),2) AS average_rating
FROM info
INNER JOIN reviews
USING(product_id)
WHERE description IS NOT NULL
GROUP BY description_length
ORDER BY description_length

--Task7:

SELECT brand ,
       EXTRACT(MONTH FROM last_visited) AS month,
       COUNT(reviews) AS num_reviews
FROM traffic
INNER JOIN reviews 
USING(product_id) 
INNER JOIN brands 
USING(product_id) 
WHERE brand IS NOT NULL 
    AND EXTRACT(MONTH FROM last_visited) IS NOT NULL
GROUP BY brand, month 
ORDER BY brand, month

--Task8:

WITH footwear AS
(
    SELECT description, revenue
    FROM info
    INNER JOIN finance
    USING(product_id)
    WHERE (description ILIKE '%shoe%'
            OR description ILIKE '%trainer%'
            OR description ILIKE '%foot%')
    AND (description IS NOT NULL)
)

SELECT COUNT(*) AS num_footwear_products, 
       PERCENTILE_DISC(0.5) WITHIN GROUP (ORDER BY revenue) AS median_footwear_revenue
FROM footwear 

--Task9:

WITH footwear AS
(
    SELECT description, revenue
    FROM info
    INNER JOIN finance
    USING(product_id)
    WHERE (description ILIKE '%shoe%'
            OR description ILIKE '%trainer%'
            OR description ILIKE '%foot%')
    AND (description IS NOT NULL)
)

SELECT COUNT(info.*) AS num_clothing_products,
       PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY revenue) AS median_clothing_revenue
FROM info
INNER JOIN finance
USING(product_id)
WHERE description NOT IN (SELECT description FROM footwear)
