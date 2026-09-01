from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score, mean_squared_error

from python.ml.preprocessing import (
    preprocess_data,
    split_data,
    prepare_features
)

def create_reg_baseline_pipeline():
    """
    Create Baseline ML model Pipeline Reuseable Function
    """

    return Pipeline(
        steps=[
            (
                "model",
                RandomForestRegressor(
                    n_estimators=100,
                    n_jobs=-1,
                    random_state=42
                )
            )
        ]
    )

    
def train_model(model_pipeline,X_train,y_train):
    """
    Function to train the model using the Pipeline
    """

    try:

        model_pipeline.fit(X_train,y_train)

        print("\n Model Trained Successfully")

        return model_pipeline

    except Exception as e:
        print(f"Issue Training Model : {e}")
        raise

def evaluate_model(model_pipeline,X,y,dataset_name):
    """
    Evaluate Trained Model against Validation and Testing Data
    """

    y_pred=model_pipeline.predict(X)

    mae=mean_absolute_error(y,y_pred) 

    rmse=mean_squared_error(
        y,
        y_pred
    ) ** 0.5

    r2 = r2_score(y,y_pred)

    print(f"\n{dataset_name} Evaluation")
    print(f"MAE:  {mae:,.2f}")
    print(f"RMSE: {rmse:,.2f}")
    print(f"R²:   {r2:.4f}")

    return {
        "mae":mae,
        "rmse":rmse,
        "r2":r2
    }

def evaluate_naive_baseline(df):
    """
    Evaluate Naive Forecast by using only previous_weekly_sales as the prediction for the current week
    """
    evaluation_df=df.dropna(subset=["previous_weekly_sales"]).copy()

    actual=evaluation_df["weekly_sales"]
    predicted=evaluation_df["previous_weekly_sales"]

    mae=mean_absolute_error(actual,predicted)

    rmse=mean_squared_error(actual,predicted) ** 0.5

    r2 = r2_score(actual,predicted)

    print("\nNaive Baseline Evaluation")
    print(f"MAE:  {mae:,.2f}")
    print(f"RMSE: {rmse:,.2f}")
    print(f"R²:   {r2:.4f}")

    return {
        "mae": mae,
        "rmse": rmse,
        "r2": r2,
    }

def run_baseline_model():
    """
    Executing the Baseline Model Training and Evaluation
    """
    df= preprocess_data()

    train_df,validation_df,test_df=split_data(df)

    naive_metrics=evaluate_naive_baseline(validation_df)


    (
        X_train,
        y_train,
        X_validation,
        y_validation,
        X_test,
        y_test
    ) = prepare_features(train_df,validation_df,test_df)

    model_pipeline=create_reg_baseline_pipeline()

    trained_model=train_model(
        model_pipeline,
        X_train,
        y_train
    )

    validation_metrics=evaluate_model(
        trained_model,
        X_validation,
        y_validation,
        "Validation"
    )

    return {
        "trained_model":trained_model,
        "validation_metrics":validation_metrics,
        "Naive_metrics":naive_metrics,
        "X_test":X_test,
        "y_test":y_test
    }



if __name__ == "__main__":
    run_baseline_model()