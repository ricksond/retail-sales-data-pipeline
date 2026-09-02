from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor,GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score, mean_squared_error
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import RandomizedSearchCV, TimeSeriesSplit

from python.ml.preprocessing import (
    preprocess_data,
    split_data,
    prepare_features
)

def create_model_pipeline(model):
    """
    Create Reusable ML model Pipeline for any Regressor Model
    """

    return Pipeline([
        ("model",model)
    ])


def get_models():
    """
    Return a dictionary of available models for training
    """

    return {

        "LinearRegression": LinearRegression(),
        "RandomForestRegressor": RandomForestRegressor(n_estimators=100, n_jobs=-1, random_state=42),
        "GradientBoostingRegressor": GradientBoostingRegressor(n_estimators=100, random_state=42)
    }

    
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

def compare_models(models,X_train,y_train,X_validation,y_validation):
    """
    Train and Evaluate Multiple Models and Compare their Performance
    """
    results={}

    for model_name, model in models.items():

        print(f"\n Training Model: {model_name}")

        pipeline=create_model_pipeline(model)

        trained_pipeline=train_model(pipeline,X_train,y_train)

        metrics=evaluate_model(
            trained_pipeline,
            X_validation,
            y_validation,
            model_name
        )

        results[model_name]=metrics
        
    return results

def run_model_comparison():
    """
    Executing the Model Comparison and Evaluation
    """
    df= preprocess_data()

    train_df,validation_df,test_df=split_data(df)

    (
        X_train,
        y_train,
        X_validation,
        y_validation,
        X_test,
        y_test
    ) = prepare_features(train_df,validation_df,test_df)

    models=get_models()

    results=compare_models(
        models,
        X_train,
        y_train,
        X_validation,
        y_validation
    )

    print("\n Model Comparison Results:")

    for model_name, metrics in results.items():
        print(f"\n {model_name}:")
        print(f" MAE:  {metrics['mae']:,.2f}")
        print(f" RMSE: {metrics['rmse']:,.2f}")
        print(f" R²:   {metrics['r2']:.4f}")
    return results

def tune_rf_model():
    """
    Tune Random Forest Model Hyperparameters and apply cross validation to train
    """
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

    model=RandomForestRegressor(n_estimators=100, n_jobs=-1, random_state=42)

    pipeline=create_model_pipeline(model)

    param_grid={
        "model__n_estimators":[100,200,300],
        "model__max_depth":[10,20,30],
        "model__min_samples_split":[2,5,10],
        "model__min_samples_leaf":[1,2,4],
        "model__max_features":["sqrt","log2",1.0]
    }

    # Create Time Based Cross Validation split with respect to sales_date
    unique_train_dates=train_df["sales_date"].sort_values().unique()

    time_splits=TimeSeriesSplit(n_splits=5)

    cv_splits=[]

    for train_date_index, val_date_index in time_splits.split(unique_train_dates):
        train_dates=unique_train_dates[train_date_index]
        val_dates=unique_train_dates[val_date_index]

        train_indices=np.flatnonzero(train_df["sales_date"].isin(train_dates).to_numpy())

        val_indices=np.flatnonzero(train_df["sales_date"].isin(val_dates).to_numpy())

        cv_splits.append((train_indices,val_indices))

   # time_split=TimeSeriesSplit(n_splits=5)

    search=RandomizedSearchCV(
        pipeline,
        param_distributions=param_grid,
        n_iter=30,
        cv=cv_splits,
        scoring="neg_mean_absolute_error",
        n_jobs=-1,
        random_state=42,
        verbose=1
    )

    search.fit(X_train,y_train)

    #Predict on Validation Set
    y_pred=search.predict(X_validation)

    val_mae=mean_absolute_error(y_validation,y_pred)

    val_rmse=mean_squared_error(y_validation,y_pred) ** 0.5

    val_r2=r2_score(y_validation,y_pred)

    # Tuned model evalaution and error analysis
    tuned_model_features=search.best_estimator_.named_steps["model"].feature_importances_

    features=pd.DataFrame({
        "feature":X_train.columns,
        "importance":tuned_model_features
    })

    feature_importance=features.sort_values(by="importance",ascending=False)


    # Residual Analysis
    residuals=y_validation-y_pred

    # Actual vs Predicted

    predictions_result=pd.DataFrame({
        "actual": y_validation.values,
        "predicted": y_pred,
        "residuals": residuals.values
    })

    predictions_result["absolute_error"]=predictions_result["residuals"].abs()


    # Plots to show predictions vs actual and residuals to better determine model performance

    # 1. Actual vs Predicted Plot
    plt.figure(figsize=(8,6))
    plt.scatter(predictions_result["actual"],predictions_result["predicted"],alpha=0.5)
    plt.xlabel("Actual Weekly Sales")
    plt.ylabel("Predicted Weekly Sales")
    plt.title("Actual vs Predicted Weekly Sales")
    plt.plot([predictions_result["actual"].min(), predictions_result["actual"].max()],
             [predictions_result["actual"].min(), predictions_result["actual"].max()],linestyle='--')
    plt.tight_layout()
    plt.savefig("docs/eda/actual_vs_predicted.png")
    plt.close()

    # 2. Residuals Plot
    # Residual Distribution
    plt.figure(figsize=(8, 6))
    plt.hist(predictions_result["residuals"], bins=30)
    plt.xlabel("Residual")
    plt.ylabel("Frequency")
    plt.title("Validation Residual Distribution")
    plt.tight_layout()
    plt.savefig("docs/eda/residual_distribution.png")
    plt.close()

    # Residuals Over Time
    plt.figure(figsize=(12, 6))
    plt.scatter(validation_df["sales_date"], predictions_result["residuals"], alpha=0.5)
    plt.axhline(y=0, color='r', linestyle='--')
    plt.xlabel("Sales Date")
    plt.ylabel("Residuals")
    plt.title("Validation Residuals Over Time")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("docs/eda/residuals_over_time.png")
    plt.close()

    # Final Model Evaluation with Testing Data
    y_test_pred=search.predict(X_test)

    test_mae=mean_absolute_error(y_test,y_test_pred)

    test_rmse=mean_squared_error(y_test,y_test_pred) ** 0.5

    test_r2=r2_score(y_test,y_test_pred)

    #Naive Test Baseline Evaluation
    naive_test_evaluation=X_test["previous_weekly_sales"].copy()

    naive_test_mae=mean_absolute_error(y_test,naive_test_evaluation)

    naive_test_rmse=mean_squared_error(y_test,naive_test_evaluation) ** 0.5

    naive_test_r2=r2_score(y_test,naive_test_evaluation)




    print("\nBest Parameters:")
    print(search.best_params_)

    print(f"\nBest CV MAE: {-search.best_score_:,.2f}")

    print(f"\nValidation MAE: {val_mae:,.2f}")
    print(f"\nValidation RMSE: {val_rmse:,.2f}")
    print(f"\nValidation R²: {val_r2:.4f}")

    print(f"\nFeature Importance:")
    print(feature_importance)

    print("\nResidual Analysis:")
    print(f"Mean Residual: {residuals.mean():,.2f}")
    print(f"Minimum Residual: {residuals.min():,.2f}")
    print(f"Maximum Residual: {residuals.max():,.2f}")
    print(f"Residual Std Dev: {residuals.std():,.2f}")

    print("\nLargest Prediction Errors:")
    print(
        predictions_result
        .sort_values("absolute_error", ascending=False)
        .head(10)
        .to_string(index=False)
    )

    print("\n Actual vs Predicted , Residuals and Residuals Over Time Plots saved in docs/eda folder.")

    print("\nFinal Test Evaluation:")
    print(f"Test MAE:  {test_mae:,.2f}")
    print(f"Test RMSE: {test_rmse:,.2f}")
    print(f"Test R²:   {test_r2:.4f}")

    print("\nNaive Test Baseline:")
    print(f"Test MAE:  {naive_test_mae:,.2f}")
    print(f"Test RMSE: {naive_test_rmse:,.2f}")
    print(f"Test R²:   {naive_test_r2:.4f}")

    return (search.best_estimator_, 
            search.best_params_, 
            search.best_score_,
            val_mae,
            val_rmse,
            val_r2, 
            test_mae,
            test_rmse,
            test_r2,
            naive_test_mae,
            naive_test_rmse,
            naive_test_r2,
            feature_importance,
             predictions_result,
             residuals)


if __name__ == "__main__":
   tune_rf_model()