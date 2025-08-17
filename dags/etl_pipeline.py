from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from scripts.wrangle_data import wrangle_car_data
from scripts.train_model import train

default_args = {
    'start_date': datetime(2025, 8, 1),
    'retries': 1,
}

def wrangle():
    df = wrangle_car_data('data/raw/cars.csv')
    df.to_csv('data/processed/cars_clean.csv', index=False)


with DAG("used_car_etl_pipeline",
         schedule_interval="@daily",
         default_args=default_args,
         catchup=False) as dag:

    wrangle_task = PythonOperator(
        task_id="wrangle_data",
        python_callable=wrangle
    )

    train_task = PythonOperator(
        task_id="train_model",
        python_callable=train
    )

    wrangle_task >> train_task

