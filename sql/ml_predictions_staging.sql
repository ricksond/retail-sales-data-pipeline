CREATE TABLE IF NOT EXISTS ml_predictions_staging (
    store_id INTEGER NOT NULL,
    sales_date DATE NOT NULL,
    weekly_sales NUMERIC(14,2),
    predicted_weekly_sales NUMERIC(14,2) NOT NULL,
    prediction_error NUMERIC(14,2),
    absolute_error NUMERIC(14,2),
    model_version VARCHAR(50) NOT NULL,
    prediction_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);