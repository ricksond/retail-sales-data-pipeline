WITH date_range AS (
    SELECT 
        MIN(sales_date) AS start_date,
        MAX(sales_date) AS end_date
    FROM {{ ref('stg_weekly_sales') }}
),

date_series AS (
    SELECT 
         generate_series(
            start_date,
            end_date,
            INTERVAL '1 day'
         ):: DATE as full_date
    FROM date_range
)

SELECT
    TO_CHAR(full_date, 'YYYYMMDD')::INTEGER as date_key,
    full_date,

    EXTRACT(YEAR FROM full_date)::INTEGER AS year,
    EXTRACT(QUARTER FROM full_date)::INTEGER AS quarter,
    EXTRACT(MONTH FROM full_date)::INTEGER AS month,
    EXTRACT(WEEK FROM full_date)::INTEGER AS week_of_year,
    EXTRACT(DAY FROM full_date)::INTEGER AS day_of_month,
    EXTRACT(DOW FROM full_date)::INTEGER AS day_of_week,

    TO_CHAR(full_date, 'Month') AS month_name,
    TO_CHAR(full_date, 'Day') AS day_name,

    CASE 
        WHEN EXTRACT(DOW FROM full_date) IN (0, 6) 
        THEN TRUE
        ELSE FALSE
    END AS is_weekend

FROM date_series


