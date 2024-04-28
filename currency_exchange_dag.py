from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import timedelta,datetime
from main import main

# UTC is default timezone for airflow so i assumed it is set that way
# it can be changed with default_timezone = 'smth' if u demand it

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 4, 24),
    'email_on_failure': '1fit@example.com',
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'timezone' : 'UTC'
}

with DAG(
    'currency_exchange_rates',
    default_args=default_args,
    description='A DAG to fetch and store currency exchange rates in PostgreSQL',
    schedule_interval='0 0 * * *',
) as dag:
    get_currencies_rate_task = PythonOperator(
        task_id='main',
        python_callable=main,
    )


    get_currencies_rate_task
    # >> some task to transform this data or smth (just a snippet for the future)
