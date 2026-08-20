SELECT 
    holiday_flag
FROM {{ ref('stg_weekly_sales') }}
WHERE holiday_flag NOT IN (0,1)