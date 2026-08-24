SELECT
     store_id,
     sales_date,
     COUNT(*) as record_count

FROM {{ref('ml_weekly_sales')}}
GROUP BY 
      store_id, 
      sales_date
HAVING COUNT(*) > 1