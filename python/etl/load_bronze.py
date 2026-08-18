import os
from pathlib import Path
import pandas as pd
from dotenv import load_dotenv
import psycopg

#load environment variables
load_dotenv()

DATA_PATH = Path("data/rawdata/Walmart.csv")

def load_bronze():
    #Extract the data from the source file
    df=pd.read_csv(DATA_PATH)

    print(f"Extracted {len(df)} records from source system.")
    #establishing the connection to the database
    connection=psycopg.connect(
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD")
    )

    try:
        with connection.cursor() as cursor:

            #clear existing bronze data before loading new data
            cursor.execute(
                "TRUNCATE TABLE bronze.sales_raw"
            )
            #load the data into the bronze table
            insert_query="""
            INSERT INTO bronze.sales_raw(
            store,
            date,
            weekly_sales,
            holiday_flag,
            temperature,
            fuel_price,
            cpi,
            unemployment
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
            """

            records=[
                tuple(row)
                for row in df.itertuples(index=False, name=None)
            ]

            cursor.executemany(insert_query, records)
        connection.commit()

        print(f"Loaded {len(records)} records into bronze.sales_raw table.")
    except Exception:
        connection.rollback()
        print("Error occurred while loading data into bronze.sales_raw table.")
        raise
    finally:
        connection.close()

if __name__ == "__main__":
    load_bronze()

