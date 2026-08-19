import os
import pandas as pd
from pathlib import Path

import psycopg

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DATA_PATH=Path("data/rawdata/Walmart.csv")

def get_connection():
    """Establish a connection to the PostgreSQL database."""
    return psycopg.connect(
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD")
    )

def validate_bronze():
    """
    Validate the data in the bronze.sales_raw table by checking for null values and duplicates.
    """

    source_df=pd.read_csv(DATA_PATH)
    print(f"Source data has {len(source_df)} records.")

    connection=get_connection()

    try:
        with connection.cursor() as cursor:

            # Query to count the number of records in the bronze.sales_raw table
            cursor.execute(
                "SELECT COUNT(*) FROM bronze.sales_raw;"
            )

            bronze_count=cursor.fetchone()[0]

            source_count=len(source_df)

            #Query to count the number of stores in the bronze.sales_raw table

            cursor.execute(
                "SELECT COUNT(DISTINCT store) FROM bronze.sales_raw;"
            )

            bronze_store_count=cursor.fetchone()[0]

            source_store_count=source_df['Store'].nunique()

            #Query to count the number of dates in the bronze.sales_raw table

            cursor.execute(
                "SELECT COUNT(DISTINCT date) FROM bronze.sales_raw;"
            )

            bronze_date_count=cursor.fetchone()[0]

            source_date_count=source_df['Date'].nunique()

            #Query to check for duplicates in the `Store + Date` grain in the bronze.sales_raw table
            cursor.execute(
                "SELECT store,date,COUNT(*) FROM bronze.sales_raw GROUP BY store,date HAVING COUNT(*) > 1"
            )

            bronze_duplicates=cursor.fetchall()

            # Query to check for null values in the bronze.sales_raw table
            cursor.execute(
                "SELECT COUNT(*) FROM bronze.sales_raw " \
                "WHERE store IS NULL " \
                "OR date IS NULL " \
                "OR weekly_sales IS NULL " \
                "OR holiday_flag IS NULL " \
                "OR temperature IS NULL " \
                "OR fuel_price IS NULL OR cpi IS NULL OR unemployment IS NULL;"
            )

            bronze_null_count=cursor.fetchone()[0]

            # Query to check if weekly_sales is negative in the bronze.sales_raw table
            cursor.execute(
                "SELECT COUNT(*) FROM bronze.sales_raw WHERE weekly_sales < 0;"
            )

            bronze_negative_sales_count=cursor.fetchone()[0]

            # Query to check if holiday_flag is not 0 or 1 in the bronze.sales_raw table
            cursor.execute(
                "SELECT COUNT(*) FROM bronze.sales_raw WHERE holiday_flag NOT IN (0, 1);"
            )

            bronze_holiday_flag_count=cursor.fetchone()[0]

            print("\n Bronze Table Validation Results:")
            print(f" - Total records: {bronze_count} (Source: {source_count})")
            print(f" - Unique stores: {bronze_store_count} (Source: {source_store_count})")
            print(f" - Unique dates: {bronze_date_count} (Source: {source_date_count})")
            print(f" - Duplicates found: {bronze_duplicates}")
            print(f" - Null values found: {bronze_null_count}")
            print(f" - Negative weekly_sales found: {bronze_negative_sales_count}")
            print(f" - Invalid holiday_flag values found: {bronze_holiday_flag_count}")

            if bronze_count != source_count:
                raise ValueError(f"Record count mismatch: Bronze({bronze_count}) vs Source({source_count})")

            if bronze_store_count != source_store_count:
                raise ValueError(f"Store count mismatch: Bronze({bronze_store_count}) vs Source({source_store_count})")

            if bronze_date_count != source_date_count:
                raise ValueError(f"Date count mismatch: Bronze({bronze_date_count}) vs Source({source_date_count})")

            if bronze_duplicates:
                raise ValueError(f"Duplicates found in bronze.sales_raw table: {bronze_duplicates}")

            if bronze_null_count != 0:
                raise ValueError(f"Null values found in bronze.sales_raw table: {bronze_null_count}")

            if bronze_negative_sales_count != 0:
                raise ValueError(f"Negative weekly_sales found in bronze.sales_raw table: {bronze_negative_sales_count}")

            if bronze_holiday_flag_count != 0:
                raise ValueError(f"Invalid holiday_flag values found in bronze.sales_raw table: {bronze_holiday_flag_count}")

            print("Bronze table validation passed successfully.")
    except Exception as e:
        print(f"Bronze Validation Failed:{e}")
        raise e
    finally:
        connection.close() 

if __name__ == "__main__":
    validate_bronze() 