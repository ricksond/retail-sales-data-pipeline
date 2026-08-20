SELECT 
     store AS store_id,
     TO_DATE(date,'DD-MM-YYYY') AS sales_date,
     weekly_sales,
     holiday_flag,
     temperature,
     fuel_price,
     cpi,
     unemployment
FROM {{ source('bronze', 'sales_raw') }} 