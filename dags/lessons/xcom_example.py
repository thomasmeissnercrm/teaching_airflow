"""
This pipeline shows how use xcoms in Airflow.

Data_in:
    Postgres:
        - europe.close_relations_2015
        - europe.gdp_2016
        - europe.low_savings_2016

Data_out: None
Depend_on: None
@author: Rafal Chmielewski
@team: Airflow Learning
@stakeholders: People who learns
"""
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.postgres_operator import PostgresOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
from airflow.models import DAG, datetime
import logging


def python_xcom(**context):
    """
    generate xcom by return statement.
    :param context:
    :return:
    """
    return 'europe.close_relations_2015'


def python_xcom2(**context):
    """
    Push xcom using function
    :param context:
    :return:
    """
    ti = context['ti']
    ti.xcom_push(key='my_xcom', value='europe.gdp_2016')


def get_xcom(**context):
    """
    retrieving xcom in python operator
    :param context:
    :return:
    """
    ti = context['ti']
    data = ti.xcom_pull(task_ids='xcom_from_bash', key='return_value')
    logging.info(data)


dag = DAG(
    dag_id='xcom_example',
    schedule_interval=None,
    start_date=datetime(2020, 1, 1),
    default_args={"owner": "airflow_lesson"}
)

start = DummyOperator(
    task_id='start',
    dag=dag
)

end = DummyOperator(
    task_id='end',
    dag=dag
)

ex1 = BashOperator(
    task_id='xcom_from_bash',
    bash_command="echo 'europe.low_savings_2016' ",
    xcom_push=True,
    dag=dag
)

ex2 = PythonOperator(
    task_id='xcom_python_return',
    python_callable=python_xcom,
    provide_context=True,
    dag=dag
)

ex3 = PythonOperator(
    task_id='xcom_python_push',
    python_callable=python_xcom2,
    provide_context=True,
    dag=dag
)

p1 = PythonOperator(
    task_id='use_xcom1',
    python_callable=get_xcom,
    provide_context=True,
    dag=dag
)

p2 = PostgresOperator(
    task_id='use_xcom2',
    sql="SELECT count(*) FROM {{ ti.xcom_pull(task_ids='xcom_python_return', key='return_value')}}",
    postgres_conn_id='airflow_docker_db',
    dag=dag
)

p3 = PostgresOperator(
    task_id='use_xcom3',
    sql="SELECT count(*) from {{ task_instance.xcom_pull(task_ids='xcom_python_push', key='my_xcom')}}",
    postgres_conn_id='airflow_docker_db',
    dag=dag
)

start >> ex1 >> p1 >> end
start >> ex2 >> p2 >> end
start >> ex3 >> p3 >> end
