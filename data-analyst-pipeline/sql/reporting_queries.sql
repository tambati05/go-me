-- Run against output/reporting.db after the pipeline completes.
-- Category revenue (stored as integer cents to avoid floating-point rounding).
SELECT product_category,
       COUNT(*) AS order_count,
       SUM(quantity) AS units_sold,
       printf('%.2f', SUM(quantity * unit_price_cents) / 100.0) AS revenue_usd
FROM orders
GROUP BY product_category
ORDER BY revenue_usd DESC;

-- Daily revenue trend.
SELECT order_date,
       COUNT(*) AS orders,
       printf('%.2f', SUM(quantity * unit_price_cents) / 100.0) AS revenue_usd
FROM orders
GROUP BY order_date
ORDER BY order_date;

-- Data quality issue counts.
SELECT reason, COUNT(*) AS rejected_records
FROM rejected_orders
GROUP BY reason
ORDER BY rejected_records DESC, reason;
