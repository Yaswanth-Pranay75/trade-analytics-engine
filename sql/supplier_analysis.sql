-- Supplier active / churned
WITH supplier_years AS (
    SELECT supplier_name, ARRAY_AGG(DISTINCT year) AS years
    FROM shipments
    GROUP BY supplier_name
)
SELECT supplier_name,
       CASE WHEN 2025 = ANY(years) THEN 'Active_2025'
            WHEN array_length(years,1) = 1 AND 2025 <> ANY(years) THEN 'Historical_only'
            WHEN 2025 <> ANY(years) AND array_length(years,1) > 0 THEN 'Churned'
            ELSE 'Unknown' END AS status,
       years
FROM supplier_years;
