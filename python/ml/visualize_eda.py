import matplotlib.pyplot as plt
import pandas as pd

from python.ml.load_dataset import load_ml_dataset
from python.utils.odbc_connection import get_odbc_connection

def visualize_eda(df:pd.DataFrame):
    """
    Create visualizations for the EDA done on the ML dataset
    """

    # 1. Weekly Sales over time

    weekly_trend=df.groupby('sales_date')['weekly_sales'].sum()

    plt.figure(figsize=(12,6))
    plt.plot(weekly_trend.index,weekly_trend.values)
    plt.title("Total Weekly Sales Over Time By Sales Date")
    plt.xlabel("Sales Date")
    plt.ylabel("Total Weekly Sales")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("docs/eda/weekly_sales_trend.png")
    plt.close()

    # 2. Average Sales by month
    monthly_sales=df.groupby('month')['weekly_sales'].mean()

    plt.figure(figsize=(10,6))
    plt.bar(monthly_sales.index,monthly_sales.values)
    plt.title("Average Weekly Sales By Month")
    plt.xlabel("Month")
    plt.ylabel("Average Weekly Sales")
    plt.tight_layout()
    plt.savefig("docs/eda/average_weekly_sales_month.png")
    plt.close()

    # 3. Average Sales by Store
    store_sales=df.groupby('store_id')['weekly_sales'].mean().sort_values(ascending=False)

    plt.figure(figsize=(12,6))
    plt.bar(store_sales.index,store_sales.values)
    plt.title("Average Weekly Sales By Store")
    plt.xlabel("Stores")
    plt.ylabel("Average Weekly Sales")
    plt.tight_layout()
    plt.savefig("docs/eda/average_weekly_sales_by_store.png")
    plt.close()

    # 4. Previous Vs Current Week Sales
    plt.figure(figsize=(8,6))
    plt.scatter(
        df['previous_weekly_sales'],
        df['weekly_sales'],
        alpha=0.6
    )
    plt.title("Previous Vs Current Week Sales")
    plt.xlabel("Previous Week Sales")
    plt.ylabel("Current Week Sales")
    plt.tight_layout()
    plt.savefig("docs/eda/previous_vs_current_week_sales.png")
    plt.close()

    # 5. Correlation Matrix
    numeric_columns=df.select_dtypes(
        include=["int64","float64"]
    )

    correlation=numeric_columns.corr()

    plt.figure(figsize=(12,10))
    plt.imshow(correlation)
    plt.colorbar()

    plt.xticks(
        range(len(correlation.columns)),
        correlation.columns,
        rotation=90
    )

    plt.yticks(
        range(len(correlation.columns)),
        correlation.columns
    )

    plt.title("Feature Correlation Matrix")
    plt.tight_layout
    plt.savefig("docs/eda/correlation_matrix_numeric_features.png")

    print("\n EDA Visualizations Generated Successfully")

if __name__ == "__main__":
    dataset=load_ml_dataset()

    visualize_eda(dataset)
