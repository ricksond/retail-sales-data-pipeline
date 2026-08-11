# Retail Sales Data Warehouse & Analytics Pipeline

## 📌 Overview

This project builds an end-to-end **retail sales data warehouse and analytics pipeline** using modern data engineering practices.

The goal is to transform raw retail sales data into clean, structured, and analytics-ready datasets through a **medallion architecture** consisting of Bronze, Silver, and Gold layers.

The project focuses on building a reliable data pipeline from raw data ingestion through transformation and orchestration, while maintaining a modular and version-controlled development workflow.

## 🎯 Project Objectives

* Build an end-to-end retail data pipeline from raw data to analytics-ready datasets.
* Implement a **medallion architecture** using Bronze, Silver, and Gold layers.
* Use **PostgreSQL** as the data warehouse.
* Use **Python** for data ingestion and processing.
* Use **dbt** for SQL-based data transformation and modeling.
* Use **Apache Airflow** to orchestrate and schedule pipeline workflows.
* Apply data quality and transformation practices to create reliable analytical datasets.
* Maintain the project using **Git and GitHub** for version control.
* Create a foundation for downstream analytics and machine learning applications.

## 🏗️ Architecture

The pipeline follows a medallion architecture:

```text
                ┌─────────────────┐
                │   Raw Retail    │
                │      Data       │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │  Bronze Layer   │
                │  Raw / Ingested │
                │      Data       │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │  Silver Layer   │
                │ Cleaned &       │
                │ Transformed Data│
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │   Gold Layer    │
                │ Analytics-Ready │
                │      Data       │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │    Analytics    │
                │  / ML Workloads │
                └─────────────────┘
```

## 🥉 Bronze Layer

The Bronze layer serves as the initial landing layer for the raw retail sales data.

Responsibilities include:

* Ingesting raw source data.
* Preserving the original structure and values where appropriate.
* Loading source data into PostgreSQL.
* Providing a reliable starting point for downstream transformations.

## 🥈 Silver Layer

The Silver layer focuses on cleaning and standardizing the raw data.

Transformations include:

* Handling missing and inconsistent values.
* Standardizing data types.
* Cleaning categorical fields.
* Removing or addressing duplicate records.
* Applying business and data quality rules.
* Creating structured datasets for downstream analysis.

## 🥇 Gold Layer

The Gold layer contains analytics-ready datasets designed for business reporting and downstream analytical workloads.

This layer focuses on:

* Business-level aggregations.
* Retail sales metrics.
* Customer and product analysis.
* Time-based sales analysis.
* Creating reusable datasets for analytics and machine learning.

## 🛠️ Technology Stack

| Technology         | Purpose                               |
| ------------------ | ------------------------------------- |
| **Python**         | Data ingestion and processing         |
| **PostgreSQL**     | Data warehouse                        |
| **SQL**            | Data querying and transformation      |
| **dbt**            | Data transformation and modeling      |
| **Apache Airflow** | Pipeline orchestration                |
| **Docker**         | Containerized development environment |
| **Git / GitHub**   | Version control                       |
| **GitHub Actions** | CI/CD and automated validation        |

## 📂 Project Structure

```text
retail-sales-data-warehouse/
│
├── airflow/
│   ├── dags/
│   │   └── .gitkeep
│   ├── logs/
│   ├── plugins/
│   │   └── .gitkeep
│   └── config/
│       └── .gitkeep
│
├── dbt/
│   ├── models/
│   │   ├── bronze/
│   │   ├── silver/
│   │   └── gold/
│   ├── tests/
│   ├── macros/
│   └── seeds/
│
├── python/
│   ├── etl/
│   ├── ml/
│   └── utils/
│
├── sql/
│   ├── database/
│   ├── schemas/
│   └── validation/
│
├── data/
│   └── raw/
│
├── tests/
│   ├── etl/
│   └── ml/
│
├── docs/
│   ├── architecture/
│   ├── data_dictionary/
│   └── setup/
│
└── .github/
    └── workflows/
```

## 🔄 Pipeline Workflow

The overall workflow is designed around the following process:

```text
Raw Data
   ↓
Python Ingestion
   ↓
PostgreSQL
   ↓
Bronze Layer
   ↓
dbt Transformations
   ↓
Silver Layer
   ↓
Business Transformations
   ↓
Gold Layer
   ↓
Analytics / Machine Learning
```

Apache Airflow is used to orchestrate the workflow and manage dependencies between pipeline tasks.

## 📊 Analytics

The Gold layer is designed to support analysis of areas such as:

* Sales performance
* Product performance
* Customer purchasing behavior
* Revenue trends
* Store or regional performance

These datasets can also serve as the foundation for future predictive modeling and machine learning applications.

## 🧪 Data Quality

Data quality is incorporated throughout the transformation process.

Examples include:

* Null-value checks
* Duplicate detection
* Data type validation
* Referential integrity
* Accepted-value validation
* dbt model tests

The objective is to ensure that downstream datasets are consistent, reliable, and suitable for analytical use.

## 🔄 Orchestration

Apache Airflow manages the execution and scheduling of pipeline workflows.

The orchestration layer is responsible for:

1. Triggering data ingestion.
2. Loading raw data into PostgreSQL.
3. Running transformation workflows.
4. Executing data quality checks.
5. Managing task dependencies.
6. Providing visibility into pipeline execution.

## 🐳 Docker

Docker is used to create a consistent local development environment for the data engineering stack.

This helps standardize the setup across services and reduces environment-specific configuration issues.

## 🌿 Version Control

Git and GitHub are used throughout the project to manage development and maintain a structured workflow.

The repository follows a development workflow where changes are developed and validated before being merged into the main branch.

## 🚀 Future Improvements

Planned improvements include:

* Expanding automated data quality checks.
* Adding additional analytical models.
* Improving pipeline monitoring and logging.
* Expanding CI/CD automation.
* Adding dashboards for business analysis.
* Using Gold-layer datasets for predictive modeling.
* Improving pipeline scalability and reliability.

## 📚 Key Learning Outcomes

Through this project, I am developing practical experience with:

* Data ingestion
* Data warehousing
* Medallion architecture
* SQL transformations
* dbt data modeling
* Workflow orchestration with Airflow
* PostgreSQL
* Docker
* Data quality
* Git-based development workflows
* CI/CD for data pipelines

## 👤 Author

**Rickson Dsouza**

Master of Science in Data Science
Virginia Commonwealth University

---

⭐ *This project is being developed as a hands-on data engineering project to build practical experience designing, transforming, orchestrating, and maintaining an end-to-end data pipeline.*
