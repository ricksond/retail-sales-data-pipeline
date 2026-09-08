SELECT
    store_id,
    sales_date,
    weekly_sales,
    predicted_weekly_sales,
    prediction_error,
    absolute_error,
    model_version,
    prediction_timestamp
FROM {{source('ml_predictions','ml_predictions_staging')}}