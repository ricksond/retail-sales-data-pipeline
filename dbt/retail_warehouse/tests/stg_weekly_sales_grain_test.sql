SELECT 
      store_id,
      sales_date,
      COUNT(*) as Total_Records

FROM {{ ref('stg_weekly_sales') }}

GROUP BY
        store_id,
        sales_date

HAVING COUNT(*) > 1