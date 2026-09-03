import joblib

from python.ml.preprocessing import (
    preprocess_data,
    split_data,
    prepare_features
)

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
        return None

def generate_predictions():
    """
    Use the above loaded model to generate predictions on the test data
    """
    model = load_model()
    if model is None:
        print("Model could not be loaded. Exiting prediction generation.")
        return None

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

    return predictions_results



if __name__ == "__main__":
    generate_predictions()