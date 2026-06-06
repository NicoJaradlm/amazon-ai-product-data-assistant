-- 1. Count products by main category
SELECT
    main_category,
    COUNT(*) AS product_count
FROM products
GROUP BY main_category
ORDER BY product_count DESC;


-- 2. Top 10 products by rating count
SELECT
    product_id,
    product_name,
    rating,
    rating_count
FROM products
ORDER BY rating_count DESC
LIMIT 10;


-- 3. Average discount by main category
SELECT
    main_category,
    ROUND(AVG(discount_percentage), 2) AS avg_discount_percentage,
    COUNT(*) AS product_count
FROM products
GROUP BY main_category
ORDER BY avg_discount_percentage DESC;


-- 4. Best rated products with enough reviews
SELECT
    product_id,
    product_name,
    main_category,
    rating,
    rating_count,
    discounted_price,
    actual_price
FROM products
WHERE rating >= 4.3
  AND rating_count >= 1000
ORDER BY rating DESC, rating_count DESC
LIMIT 20;


-- 5. Review count by main category
SELECT
    p.main_category,
    COUNT(r.review_id) AS review_count
FROM reviews r
JOIN products p
    ON r.product_id = p.product_id
GROUP BY p.main_category
ORDER BY review_count DESC;


-- 6. Products with biggest absolute discount
SELECT
    product_id,
    product_name,
    main_category,
    actual_price,
    discounted_price,
    actual_price - discounted_price AS discount_amount,
    discount_percentage
FROM products
ORDER BY discount_amount DESC
LIMIT 20;