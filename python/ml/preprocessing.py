import pandas as pd

from python.ml.load_dataset import load_ml_dataset


def preprocess_data():
    """
    Load the ML Dataset and Prepare the data for ML
    """

    #invoke the load dataset function
    df=load_ml_dataset()

    print("\n Dataset Loaded Successfully!")
    print(f"\n Dataset Shape: {df.shape}")

    # convert sales_date dtype to datetime
    df["sales_date"]=pd.to_datetime(df["sales_date"])

    #Sort Dataset by store_id and Sales_date
    df=df.sort_values(
        by=['sales_date','store_id']
    ).reset_index(drop=True)

    print("\n Datetime Conversion And Sorting Completed Successfully")

    print(f"\n Sales Date Feature Dtype:{df['sales_date'].dtype} ")

    print("\n First 5 Records:")
    print(df[['store_id','sales_date','weekly_sales']].head(5))

    # Remove rows without historical sales data
    lag_features=[
        "previous_weekly_sales",
        "previous_2_weekly_sales",
        "previous_4_weekly_sales",
        "previous_year_weekly_sales"
    ]

    #Rows before filtering
    before_rows=len(df)

    # drop missing values columns
    df=df.dropna(
        subset=lag_features
    ).reset_index(drop=True)

    #Rows after filtering
    after_rows=len(df)

    print("\n Lag Features Successfully Filtered")
    print(f"\n Rows Before Filtering:{before_rows}")
    print(f"\n Rows After Filtering: {after_rows}")
    print(f"\n Rows Removed: {before_rows - after_rows}")

    #Print remaining missing values
    print(df[lag_features].isnull().sum())

    return df

def split_data(df):
    """
    Split the Dataset chronologically into training,testing and validation sets
    """

    unique_dates=sorted(df['sales_date'].unique())

    train_end=unique_dates[int(len(unique_dates) * 0.70)]
    validation_end=unique_dates[int(len(unique_dates) * 0.85)]

    train_df=df[df['sales_date'] <= train_end].copy()

    validation_df=df[
        (df['sales_date'] > train_end) &
        (df['sales_date'] <= validation_end)
    ].copy()

    test_df=df[
        df['sales_date'] > validation_end
    ].copy()

    print("\n Chronological Split Completed")

    print("\n Training:")
    print(f"Rows: {len(train_df)}")
    print(f"\n Dates Range: {train_df['sales_date'].min()} -> {train_df['sales_date'].max()}")

    print("\n Validation:")
    print(f"Rows: {len(validation_df)}")
    print(f"\n Dates Range: {validation_df['sales_date'].min()} -> {validation_df['sales_date'].max()}")

    print("\n Testing:")
    print(f"Rows: {len(test_df)}")
    print(f"\n Dates Range: {test_df['sales_date'].min()} -> {test_df['sales_date'].max()}")

    return train_df,validation_df,test_df


def prepare_features(train_df,validation_df,test_df):
    """
    Separate ML features from the target variable
    """

    #Target
    target = "weekly_sales"

    # Predictors
    features = [
        "store_id",
        "holiday_flag",
        "temperature",
        "fuel_price",
        "cpi",
        "unemployment",
        "year",
        "quarter",
        "month",
        "week_of_year",
        "previous_weekly_sales",
        "previous_2_weekly_sales",
        "previous_4_weekly_sales",
        "previous_year_weekly_sales"
    ]

    X_train=train_df[features]
    y_train=train_df[target]

    X_validation=validation_df[features]
    y_validation=validation_df[target]

    X_test=test_df[features]
    y_test=test_df[target]

    print("\n Feature And Target Separation Completed")

    print(f"\n X_train Shape: {X_train.shape}")
    print(f"y_train Shape: {y_train.shape}")

    print(f"\n X_validation Shape: {X_validation.shape}")
    print(f"y_validation Shape: {y_validation.shape}")

    print(f"\n X_test Shape: {X_test.shape}")
    print(f"y_test Shape: {y_test.shape}")

    print("\n Features:")

    print(X_train.columns.tolist())

    return (
        X_train,
        y_train,
        X_validation,
        y_validation,
        X_test,
        y_test
    )

def validate_ml_features(X_train,y_train,X_validation,y_validation,X_test,y_test):
    """
    Validate Final ML Features Sets
    """

    datasets = {
        "X_train": X_train,
        "y_train": y_train,
        "X_validation": X_validation,
        "y_validation": y_validation,
        "X_test": X_test,
        "y_test": y_test
    }

    print("\n ML Feature Final Validation")

    for name,data in datasets.items():
        print(f"\n {name}:")
        print(f"\n Shape: {data.shape} ")
        print(f"\n Missing Values: {data.isnull().sum().sum()}")

     # Validate target values
    if (y_train <= 0).any():
        raise ValueError("Invalid weekly_sales values found in training data.")

    if (y_validation <= 0).any():
        raise ValueError("Invalid weekly_sales values found in validation data.")

    if (y_test <= 0).any():
        raise ValueError("Invalid weekly_sales values found in test data.")

if __name__ == "__main__":
    df=preprocess_data()

    train_df,validation_df,test_df=split_data(df)

    (
        X_train,
        y_train,
        X_validation,
        y_validation,
        X_test,
        y_test
    ) = prepare_features(train_df,validation_df,test_df)


    validate_ml_features(
        X_train,
        y_train,
        X_validation,
        y_validation,
        X_test,
        y_test
    )