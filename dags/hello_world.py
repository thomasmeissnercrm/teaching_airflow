from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.models import DAG
import datetime
import logging


def say_hello(**context):
    logging.info(f'Everything Works! {datetime.datetime.now()}')


dag = DAG(
    dag_id='hello_world',
    schedule_interval=None,
    start_date=datetime.datetime(2020, 1, 1),
    default_args={"owner": "airflow_lesson"}
)

start = DummyOperator(
    task_id='start_dag',
    dag=dag
)

hello = PythonOperator(
    task_id='say_hello',
    python_callable=say_hello,
    provide_context=True,
    dag=dag
)

end = DummyOperator(
    task_id='end_dag',
    dag=dag
)

start >> hello >> end
