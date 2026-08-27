import pandas as pd

from python.ml.load_dataset import load_ml_dataset
from python.utils.odbc_connection import get_odbc_connection

def perform_eda(df: pd.DataFrame):
    """
    Perform exploratory data analysis on the ML dataset
    """

    print("\n =====================Exploratory Data analysis============================")

    # 1. Dataset Overview
    print("\n Dataset Shape:")
    print(df.shape)

    print("\n Columns:")
    print(df.columns)


    # Sales by store

    store_sales=df.groupby('store_id')['weekly_sales'].agg(['mean','median','min','max','sum']).sort_values('mean', ascending=False)

    print("\n TOP 10 Stores By Average Weekly Sales:")
    print(store_sales.head(10))


    # Holiday analysis
    holiday_sales=df.groupby('holiday_flag')['weekly_sales'].agg(['mean','median','count'])

    print("\n Sales by Holiday Analysis:")
    print(holiday_sales)


    # Yearly sales

    yearly_sales=df.groupby('year')['weekly_sales'].agg(['mean','median','sum'])

    print("\n Yearly Sales:")
    print(yearly_sales)


    # Monthly sales (Average)

    monthly_sales=df.groupby('month')['weekly_sales'].mean().sort_values(ascending=False)

    print("\n Average Monthly Sales:")
    print(monthly_sales)

    # Correlation Analysis

    numeric_columns=df.select_dtypes(
        include=["int64","float64"]
    )

    correlation=numeric_columns.corr()["weekly_sales"].sort_values(ascending=False)

    print("\n Correlation in weekly sales:")
    print(correlation)


    # Highest and Lowest Sales
    highest_sales=df.loc[
        df["weekly_sales"].idxmax()
    ]

    lowest_sales=df.loc[
        df["weekly_sales"].idxmin()
    ]

    print("\n Highest Weekly Sales")
    print(highest_sales)

    print("\n Lowest Weekly Sales")
    print(lowest_sales)

if __name__ == "__main__":
    dataset=load_ml_dataset()

    perform_eda(dataset)


