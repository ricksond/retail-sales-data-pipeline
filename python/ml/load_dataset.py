import pandas as pd

from python.utils.odbc_connection import get_odbc_connection


def load_ml_dataset():
    """
    Load the ML dataset from the Gold layer into a Pandas dataframe
    """

    query="""
         SELECT *
         FROM gold.ml_weekly_sales
         ORDER BY store_id, sales_date;
    """

    connection= None

    try:
        connection=get_odbc_connection()

        df=pd.read_sql(query,connection)

        print("Dataset Loaded Successfully")
        print(f"Rows:{len(df)}")
        print(f"Columns:{len(df.columns)}")

        return df

    except Exception as e:
         print(f"Failed to Load ML dataset: {e}")
         raise

    finally:
        if connection is not None:
            connection.close()
            print("Database connection closed.")

if __name__== "__main__":

    df=load_ml_dataset()

    print("\n Dataset Shape:")
    print(df.shape)

    print("\n Dataset Columns:")
    print(df.columns.tolist())

    print("\n First 5 Rows:")
    print(df.head)