WITH hsn_totals AS (
    SELECT hsn_code, SUM(total_value_inr) AS total_value_inr
    FROM shipments
    GROUP BY hsn_code
),
ranked AS (
    SELECT hsn_code, total_value_inr,
           total_value_inr * 1.0 / SUM(total_value_inr) OVER () AS share_of_total,
           SUM(total_value_inr) OVER (ORDER BY total_value_inr DESC) * 1.0 / SUM(total_value_inr) OVER () AS cumulative_share,
           ROW_NUMBER() OVER (ORDER BY total_value_inr DESC) AS rn
    FROM hsn_totals
)
SELECT CASE WHEN rn <= 25 THEN hsn_code ELSE 'OTHERS' END AS hsn_bucket,
       SUM(total_value_inr) AS total_value_inr,
       SUM(share_of_total) AS share_of_total
FROM ranked
GROUP BY CASE WHEN rn <= 25 THEN hsn_code ELSE 'OTHERS' END
ORDER BY total_value_inr DESC;
