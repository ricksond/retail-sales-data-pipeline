import joblib

from python.ml.preprocessing import (
    preprocess_data,
    split_data,
    prepare_features
)

from python.utils.database import get_connection 

MODEL_PATH="python/ml/artifacts/random_forest_model.joblib"

def load_model():
    """
    Load the Saved Best Model from the specified path.
    """

    try:

        model=joblib.load(MODEL_PATH)

        print("\nModel loaded successfully From Path")

        return model
    except Exception as e:
        print(f"\nError loading model: {e}")
        raise

def generate_predictions():
    """
    Use the above loaded model to generate predictions on the test data
    """
    model = load_model()

    df = preprocess_data()

    train_df,validation_df,test_df = split_data(df)

    (X_train,
     y_train,
     X_validation,
     y_validation,
     X_test,
     y_test) = prepare_features(train_df, validation_df, test_df)

    y_pred = model.predict(X_test)

    # Create a DataFrame to store the predictions along with the corresponding test data
    predictions_results=test_df[['store_id','sales_date','weekly_sales']].copy()

    predictions_results['predicted_weekly_sales'] = y_pred

    predictions_results["prediction_error"]= (
        predictions_results["weekly_sales"] - predictions_results["predicted_weekly_sales"]
    )

    predictions_results["absolute_error"]=predictions_results["prediction_error"].abs()

    predictions_results["model_version"]="random_forest_v1"

    print("\nPredictions generated successfully on the test data.")
    print(f"\nPredictions: {len(y_pred)}")

    print("\nPrediction DataFrame created successfully")
    print(f"Rows: {len(predictions_results)}")
    print("\nPrediction Results:")
    print(predictions_results.head(20))

    load_predictions(predictions_results)

    return predictions_results

# Function to load the predictions into the data warehouse
def load_predictions(predictions_results):
    """
    Load the predictions into the data warehouse.
    """

    connection = get_connection()
    if connection is None:
        print("Database connection could not be established. Exiting prediction loading.")
        return

    try:
        insert_query ="""
            INSERT INTO ml_predictions_staging (
                store_id,
                sales_date,
                weekly_sales,
                predicted_weekly_sales,
                prediction_error,
                absolute_error,
                model_version
            ) VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        records=predictions_results[
            [
            "store_id",
            "sales_date",
            "weekly_sales",
            "predicted_weekly_sales",
            "prediction_error",
            "absolute_error",
            "model_version"
            ]
        ].itertuples(index=False, name=None)

        with connection.cursor() as cursor:
            cursor.executemany(insert_query, records)

        connection.commit()

        print("\nPredictions loaded into the data warehouse successfully."
              f"\nTotal Records Inserted: {len(predictions_results)} INTO Table: ml_predictions_staging"
              )
    except Exception as e:
        connection.rollback()
        print(f"\nError occurred while loading predictions into the data warehouse: {e}")
        raise
    finally:
        connection.close()
        print("\nDatabase connection closed after loading predictions.")





if __name__ == "__main__":
    generate_predictions()