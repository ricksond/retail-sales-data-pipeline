-- This test checks that all sales_date values in the fct_weekly_sales table have a corresponding entry in the dim_date table.
SELECT
     f.store_id,
     f.sales_date


FROM {{ ref('fct_weekly_sales') }} as f

LEFT JOIN {{ ref('dim_date') }} as d
    ON f.sales_date = d.full_date

WHERE d.date_key IS NULL