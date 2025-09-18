import os 
import sys
from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from scripts.sales_performance import run_regression

default_args = {
    'owner': 'wawex',
    'depends_on_past': True,
    'start_date': datetime(2025, 9, 18),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'catchup': True
}

with DAG(dag_id="sales_performance_regression", default_args = default_args, 
           schedule='@daily', catchup=False)as dag:
    
    regression_task = PythonOperator(
        task_id ="run_regression_models", python_callable=run_regression,
         op_args=["../data/processed_amazon_products.csv", "../reports/regression"],
    )



















