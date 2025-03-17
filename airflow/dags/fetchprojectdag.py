from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
import os

sys.path.append('/usr/local/airflow')

from app import fetch_and_store_projects

default_args = {
    'owner': 'tung',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
with DAG(
  
    dag_id='gitlab_project_fetch_dag',
    description='Fetch GitLab projects and store them in the database',
    default_args=default_args,
    start_date=datetime(2025, 3, 1),
    schedule_interval='@hourly',
    catchup=False, 
    is_paused_upon_creation=False  
) as dag:

   
    fetch_projects_task = PythonOperator(
        task_id='fetch_gitlab_projects',
        python_callable=fetch_and_store_projects
    )


    fetch_projects_task
