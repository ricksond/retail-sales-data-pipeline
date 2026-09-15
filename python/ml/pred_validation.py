from python.utils.database import get_connection

def validate_predictions():
    """
    Validation Script for the gold Layer final prediction table and reporting
    """
    connection= None
    
    connection = get_connection()

    if connection is None:
        raise RuntimeError('Database Connection could not be established')

    try:
        with connection.cursor() as cursor:

            #1. Compare Row counts of Gold Layer Predictions table and Staging Predictions table
            cursor.execute(
                """
                SELECT COUNT(*) 
                FROM gold.ml_predictions;
                """
            )
            gold_pred_count=cursor.fetchone()[0]

            cursor.execute(
                """
                SELECT COUNT(*) 
                FROM ml_predictions_staging;
                """
            )

            staging_count=cursor.fetchone()[0]

            print(f"Staging Predictions Table Count: {staging_count}")
            print(f"Gold Layer Predictions Table Count: {gold_pred_count}")

            if staging_count==0:
                raise ValueError("ML Predictions Staging Table is Empty")
            if staging_count != gold_pred_count:
                raise ValueError(
                    f"Row Count Mismatch: staging:{staging_count}, gold layer Predictions: {gold_pred_count}"
                )

            # 2. Check for Duplicate Keys
            cursor.execute(
                """
                SELECT COUNT(*)
                FROM (
                SELECT store_id,
                       sales_date,
                       model_version
                FROM gold.ml_predictions
                GROUP BY store_id,sales_date,model_version
                HAVING COUNT(*)>1            
                ) duplicates;
                """
            )

            dupes=cursor.fetchone()[0]

            print(f"Duplicate Predictions Keys Found: {dupes}")

            if dupes !=0:
                raise ValueError("Duplicates Prediction keys Found. Resolve Prediction Idempotency Code")
            
            #3. Check for NULL Values
            cursor.execute(
                """
                SELECT COUNT(*)
                FROM gold.ml_predictions
                WHERE store_id IS NULL
                     OR sales_date IS NULL
                     OR weekly_sales IS NULL
                     OR predicted_weekly_sales IS NULL
                     OR prediction_error IS NULL
                     OR absolute_error IS NULL
                     OR model_version IS NULL
                """
            )

            nulls_count=cursor.fetchone()[0]

            if nulls_count !=0:
                raise ValueError("Null Values Found. Check for Null relevance")
            print(f"Nulls Found: {nulls_count}")

            #5.Check all staging records are present in gold layer predictions table

            cursor.execute(
                """
                SELECT COUNT(*)
                FROM ml_predictions_staging s
                LEFT JOIN gold.ml_predictions g
                        ON s.store_id = g.store_id
                        AND s.sales_date = g.sales_date
                        AND s.model_version = g.model_version
                WHERE g.store_id IS NULL
                """
            )

            gold_records_miss=cursor.fetchone()[0]

            if gold_records_miss != 0:
                raise ValueError(f"Staging Records Missing From Gold : {gold_records_miss}")
            print("No Missing Staging Records Found in Gold")

            #6. Check Prediction Date Range
            cursor.execute(
                """
                SELECT
                       MIN(sales_date),
                       MAX(sales_date)
                FROM gold.ml_predictions;
                """
            )

            min_date,max_date=cursor.fetchone()

            print(f"Predictions Dates Range FROM {min_date} --> {max_date}")

            print("\n Gold Layer Prediction Table Validated Successfully")

    except Exception as e:
        print(f"Prediction Validation Failed: {e}")
        raise
    finally:
        cursor.close()
        if connection is not None:
            connection.close()
            print("\n Database Connection Closed Succesffuly")

if __name__ == "__main__":
    validate_predictions()
