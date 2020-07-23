"""
This is test pipeline to see if airflow is working properly

Data_in: None
Data_out: None
Depend_on: None
@author: Rafal Chmielewski
@team: Airflow Learning
@stakeholders: People who learns
"""
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.models import DAG
import datetime
import logging


def say_hello(**context):
    """
    Function is puting example string into task log.
    :param context:
    :return:
    """
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
    dag=dag
)

end = DummyOperator(
    task_id='end_dag',
    dag=dag
)

start >> hello >> end
