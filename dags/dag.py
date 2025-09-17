import os 
import sys
from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from scripts.preprocessing import preprocess_data
from scripts.eda import run_eda


default_args = {
    'owner': 'wawex',
    'depends_on_past': True,
    'start_date': datetime(2025, 9, 15),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'catchup': True
}


with DAG(dag_id="amazon_product_project", default_args=default_args, schedule='@daily',
                description='ETL pipeline for Amazon Product dataset',  catchup=False,) as dag:
    
    preprocess_task = PythonOperator(
        task_id = "preprocess_amazon_data",
        python_callable=preprocess_data,
        op_args=["../data/amazon_products_sales.csv", "..data/processed_amazon_products.csv"],
    )
    
    eda_task = PythonOperator(
        task_id="eda_amazon",
        python_callable=run_eda,
        op_args=["../data/processed_amazon_products.csv", "../reports/eda"],
    )

preprocess_task >> eda_task















