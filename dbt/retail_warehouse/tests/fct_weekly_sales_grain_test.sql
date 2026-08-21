SELECT 
    store_id,
    sales_date,
    COUNT(*) AS record_count

FROM {{ ref('fct_weekly_sales') }}

GROUP BY 
    store_id,
    sales_date

HAVING COUNT(*) > 1