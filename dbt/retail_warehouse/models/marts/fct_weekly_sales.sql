SELECT
     d.date_key,
     f.store_id,
     f.sales_date,
     f.weekly_sales,
     f.holiday_flag,
     f.temperature,
     f.fuel_price,
     f.cpi,
     f.unemployment

FROM {{ ref('stg_weekly_sales') }} as f

LEFT JOIN {{ ref('dim_date') }} as d
    ON f.sales_date = d.full_date