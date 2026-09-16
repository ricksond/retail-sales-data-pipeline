# Medallion Architecture

## Overview

The project follows the Medallion Architecture consisting of
Bronze, Silver, and Gold layers.

## Bronze

Purpose: Preserve source data in its original structure.

Table:

- bronze.sales_raw

## Silver

Purpose: Clean, standardize, and validate the source data.

Table:

- silver.weekly_sales

Key transformations:

- Convert Date from string to DATE.
- Standardize column names.
- Validate numeric values.
- Validate Holiday_Flag.
- Validate Store + Date uniqueness.

## Gold

Purpose: Provide business-ready and machine-learning-ready datasets.

Tables:

- gold.dim_date
- gold.dim_store
- gold.fact_weekly_sales
- gold.sales_features

## Data Flow

Kaggle
→ Python ETL
→ Bronze
→ dbt
→ Silver
→ dbt
→ Gold
→ Python Machine Learning