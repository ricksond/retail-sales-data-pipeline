import pandas as pd
from pathlib import Path


#declare the path to the source data and create a variable to hold the path

DATA_PATH = Path("data/rawdata/Walmart.csv")


# function to inspect the source data to check for missing values, data types, and basic statistics
def inspect_source_data(path:Path) -> None:
    """
    Inspect the source data to check for missing values, data types, and basic statistics.

    Args:
        path (Path): The path to the source data file.
    """
    df=pd.read_csv(path)
    # print the shape of the data
    print("\n Shape of the data:")
    print(df.shape)

    # print the data types of the columns
    print("\n Data types of the columns:")
    print(df.dtypes)

    # print the number of missing values in each column
    print("\n Number of missing values in each column:")
    print(df.isnull().sum())

    # print the basic statistics of the numerical columns
    print("\n Basic statistics of the numerical columns:")
    print(df.describe())

    #Print the duplicate rows in the data
    print("\n Duplicate rows in the data:")     
    print(df.duplicated().sum())

    # print te uniqueness of the `Store + Date` grain 
    print("\n Uniqueness of the `Store + Date` grain:")
    duplicate_keys=df.duplicated(subset=['Store', 'Date']).sum()
    print(f"Number of duplicate `Store + Date` keys: {duplicate_keys}")

    #Determining the Date Range and to check if a store has roughly the same number of records as other stores
    df['Date']=pd.to_datetime(df['Date'],dayfirst=True)

    print("\n Date Range of the data:")
    print(f"Start Date: {df['Date'].min()}")
    print(f"End Date: {df['Date'].max()}")

    print("\n Records Per Store")
    print(df.groupby('Store').size())

    #Print the sample of the data
    print("\n Top 10 Sample of the data:")
    print(df.head(10))

#run the function to inspect the source data
if __name__ == "__main__":
    inspect_source_data(DATA_PATH)
