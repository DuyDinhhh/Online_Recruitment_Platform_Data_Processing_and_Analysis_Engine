
from airflow import DAG
from datetime import datetime
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator, BranchPythonOperator

dag = DAG(
    'etl_pipeline',
    description='A simple ETL pipeline DAG',
    schedule_interval='*/2 * * * *',  # Run every 20 minutes
    start_date=datetime(2024, 3, 20),
    catchup=False,
)

def task3_function():
    print("No new data found")


commands_task1 = """    
cd /opt/airflow/dags;
result=$(python3 check_new_data.py | tail -n 1)
echo $result
"""

commands_task2 = """
cd /opt/airflow/dags;
python3 etl_spark_job.py;
"""

task1 = BashOperator(
    task_id='check_new_data',
    bash_command=commands_task1,
    dag=dag,
)

task2 = BashOperator(
    task_id='etl_job',
    bash_command=commands_task2,
    dag=dag,
)

task3 = PythonOperator(
    task_id='handle_no_new_data',
    python_callable=task3_function,
    dag=dag,
)

def branch_function(ti):
    task1_result = ti.xcom_pull(task_ids='check_new_data').strip()
    print(f"Task 1 Result: '{task1_result}'")  # Debugging print
    if 'true' in task1_result:
        return 'etl_job'
    else:
        return 'handle_no_new_data'

branch_task = BranchPythonOperator(
    task_id='decide_next_task',
    python_callable=branch_function,
    dag=dag,
)


task1 >> branch_task
branch_task >> [task2, task3]

