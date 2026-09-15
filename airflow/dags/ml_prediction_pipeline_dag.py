from datetime import datetime

from airflow.sdk import DAG
from airflow.providers.standard.operators.python import PythonOperator
from airflow.providers.standard.operators.bash import BashOperator

from python.etl.load_bronze import load_bronze
from python.etl.validate_bronze import validate_bronze


#Dag to orechestrate the above functions
with DAG(
    dag_id="ml_prediction_pipeline_dag",
    start_date=datetime(2026,1,1),
    schedule=None,
    catchup=False,
    tags=["retail","data engineering"]
) as dag:

    ingestion_tasks=PythonOperator(
        task_id="ingest_data",
        python_callable=load_bronze
    )

    validation_tasks=PythonOperator(
        task_id="validate_bronze",
        python_callable= validate_bronze
    )

    dbt_silver_task=BashOperator(
        task_id="dbt_silver",
        bash_command="""
        cd /opt/airflow/project/dbt/retail_warehouse &&
        dbt run --select stg_weekly_sales &&
        dbt test --select stg_weekly_sales
        """
    )

    dbt_gold_task=BashOperator(
        task_id="dbt_gold",
        bash_command="""
        cd /opt/airflow/project/dbt/retail_warehouse &&
        dbt build --select fct_weekly_sales dim_date ml_weekly_sales
        """
    )

    prediction_task=BashOperator(
        task_id="generate_predictions",
        bash_command="""
        python /opt/airflow/project/python/ml/predict.py
        """
    )

    dbt_gold_predictions_task=BashOperator(
        task_id="dbt_ml_predictions",
        bash_command="""
        cd /opt/airflow/project/dbt/retail_warehouse &&
        dbt build --select ml_predictions
        """
    )

    predictions_validation_task=BashOperator(
        task_id="validate_predictions",
        bash_command="""
        python /opt/airflow/project/python/ml/pred_validation.py
        """
    )

    ingestion_tasks >> validation_tasks >> dbt_silver_task >> dbt_gold_task >> prediction_task >> dbt_gold_predictions_task >> predictions_validation_task