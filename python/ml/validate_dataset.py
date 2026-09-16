import pandas as pd

from python.ml.load_dataset import load_ml_dataset

from python.utils.odbc_connection import get_odbc_connection

def validate_dataset(df: pd.DataFrame):
    """
    Validate the dataset before model development
    """

    print("\n============== DATASET VALIDATION===================")

    # Shape
    print(f"\n Dataset Shape: {df.shape}")

    # Data Types
    print("\n Data types of Columns:")
    print(df.dtypes)

    # Missing Values
    print("\n Present Dataset Missing Values:")
    print(df.isna().sum())

    # Data + store grain dublicates
    duplicates=df.duplicated(
        subset=['store_id','sales_date']
    ).sum()

    print(f"\n Duplicate Store + Date records: {duplicates}")

    # Store Count

    print(f"Number of Stores:{df["store_id"].nunique()}")

    # Date Range
    print(f"First Date: {df['sales_date'].min()}")
    print(f"Last Date:{df['sales_date'].max()}")

    # Target Statistics
    print("\n Weekly sales statistics:")
    print(df['weekly_sales'].describe())

    lag_columns=[
        "previous_weekly_sales",
        "previous_2_weekly_sales",
        "previous_4_weekly_sales",
        "previous_year_weekly_sales"
    ]

    print("\n feature availability:")

    for column in lag_columns:
        available=df[column].notna().sum()
        missing=df[column].isna().sum()

        print (
            f"{column}: "
            f"{available} available,"
            f"{missing} missing"
        )

        # Validation Checks
        if duplicates > 0:
            raise ValueError(
                "Duplicate Store + Date records found."
            )

        # Store Uniqueness Check

        if df['store_id'].nunique() != 45:
            raise ValueError(
                "Unexpected Number of Stores"
            )

        if len(df) != 6435:
            raise ValueError(
                "Unexpected Number of Records"
            )

        print("\n Dataset Validation Passed.")

if __name__== "__main__":
    dataset=load_ml_dataset()

    validate_dataset(dataset)