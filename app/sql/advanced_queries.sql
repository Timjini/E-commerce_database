-- Vendor Profitability
-- Highest Operational costs
SELECT v.id AS vendor_id, v.company_name, 
       SUM(r.commission_amount) AS total_revenue,
       SUM(c.cost_amount) AS total_costs,
       (SUM(r.commission_amount) - SUM(c.cost_amount)) AS net_profit
FROM vendors v
JOIN revenue r ON v.id = r.vendor_id
JOIN costs c ON r.order_id = c.order_id
GROUP BY v.id, v.company_name
HAVING net_profit < 0
ORDER BY net_profit ASC;

--  highest number of operational issues
SELECT v.id AS vendor_id, v.company_name,
       COUNT(c.id) AS num_issues
FROM vendors v
JOIN revenue r ON v.id = r.vendor_id
JOIN costs c ON r.order_id = c.order_id
WHERE c.type IN ('delivery_failure', 're_attempt', 'return_fraud')
GROUP BY v.id, v.company_name
ORDER BY num_issues DESC
LIMIT 10;

-- Shopper Engagement 
-- second purchase members
SELECT s.id AS shopper_id, s.first_name, s.last_name, 
       COUNT(o.id) AS total_orders, 
       MAX(o.created_at) AS last_order_date
FROM shoppers s
JOIN orders o ON s.id = o.shopper_id
WHERE s.is_member = TRUE
GROUP BY s.id
HAVING total_orders > 1
ORDER BY last_order_date DESC;

-- time spent on the portal 
SELECT s.id AS shopper_id, 
       SUM(t.duration_minutes) AS total_time_spent
FROM shoppers s
JOIN time_spent t ON s.id = t.shopper_id
WHERE s.is_member = TRUE
GROUP BY s.id
ORDER BY total_time_spent DESC
LIMIT 10;

-- Product Performance 
-- products with the highest sales
SELECT p.id AS product_id, p.name AS product_name,
       SUM(oi.quantity) AS total_sales
FROM products p
JOIN vendor_products vp ON p.id = vp.product_id
JOIN order_items oi ON vp.id = oi.vendor_product_id
GROUP BY p.id, p.name
ORDER BY total_sales DESC
LIMIT 10;

-- products with high profitability
SELECT p.id AS product_id, p.name AS product_name,
       SUM(oi.quantity * oi.price) AS total_revenue,
       SUM(c.cost_amount) AS total_costs,
       (SUM(oi.quantity * oi.price) - SUM(c.cost_amount)) AS net_profit
FROM products p
JOIN vendor_products vp ON p.id = vp.product_id
JOIN order_items oi ON vp.id = oi.vendor_product_id
JOIN costs c ON oi.order_id = c.order_id
GROUP BY p.id, p.name
HAVING net_profit > 0
ORDER BY net_profit DESC
LIMIT 10;