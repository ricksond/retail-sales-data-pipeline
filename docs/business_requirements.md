# Business Requirements

## Project

Enterprise Retail Sales Pipeline

## Business Problem

The objective is to build a reliable retail data pipeline that
consolidates historical sales, store, department, promotional,
holiday, and economic data into a centralized PostgreSQL warehouse.

The resulting analytical dataset will support sales performance
analysis and predictive modeling of future retail sales.

## Business Objectives

1. Centralize historical retail data.
2. Establish a Medallion Architecture using Bronze, Silver, and Gold layers.
3. Create reliable and reusable SQL transformations using dbt.
4. Orchestrate the pipeline using Apache Airflow.
5. Produce a trusted Gold dataset for analytics and machine learning.
6. Develop a Python-based predictive model for future sales.

## Stakeholders

- Retail Operations
- Inventory Planning
- Marketing
- Executive Management

## Key Business Questions

### Sales Performance
- Which stores generate the highest sales?
- Which departments perform best?
- How do sales change over time?

### Store Performance
- Which stores consistently outperform others?
- Does store size relate to sales?

### External Factors
- How do holidays affect sales?
- How do fuel prices, CPI, and unemployment relate to sales?

### Promotions
- How do promotional periods affect sales?

### Predictive Analytics
- Can historical sales and business factors be used to predict future sales?

## Data Source

Walmart Store Sales Dataset from Kaggle.

Source:
https://www.kaggle.com/datasets/yasserh/walmart-dataset

## Architecture

Raw Source
→ Bronze
→ Silver
→ Gold
→ Machine Learning Dataset

## Technology Stack

- Python
- PostgreSQL
- SQL
- dbt Core
- Apache Airflow
- Docker
- Git
- GitHub
- GitHub Actions
- Spyder