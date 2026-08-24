WITH sales as (
    SELECT 
        f.store_id,
        f.sales_date,
        f.holiday_flag,
        f.temperature,
        f.fuel_price,
        f.cpi,
        f.unemployment,
        f.weekly_sales,

        d.year,
        d.quarter,
        d.month,
        d.week_of_year

    FROM {{ref('fct_weekly_sales')}} f

    INNER JOIN {{ref('dim_date')}} d
        ON f.sales_date = d.full_date
),

features as (
    SELECT
        *,
        LAG(weekly_sales, 1) OVER (PARTITION BY store_id ORDER BY sales_date) AS previous_weekly_sales,
        LAG(weekly_sales, 2) OVER (PARTITION BY store_id ORDER BY sales_date) AS previous_2_weekly_sales,
        LAG(weekly_sales, 4) OVER (PARTITION BY store_id ORDER BY sales_date) AS previous_4_weekly_sales,
        LAG(weekly_sales,52) OVER (PARTITION BY store_id ORDER BY sales_date) AS previous_year_weekly_sales
    FROM sales
)

SELECT *
FROM features