"""
This pipeline shows how templating works.

Data_in: None
Data_out: None
Depend_on: None
@author: Rafal Chmielewski
@team: Airflow Learning
@stakeholders: People who learns
"""
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.postgres_operator import PostgresOperator
from airflow.operators.python_operator import PythonOperator
from airflow.models import DAG, datetime
import random

table = 'public.log'


def fn_generate_xcom(**context):
    """
    generate xcom by xcom_push function
    :param context:
    :return:
    """
    ti = context['ti']
    ti.xcom_push(key='my_xcom', value='2+2')


dag = DAG(
    dag_id='template_example',
    schedule_interval=None,
    start_date=datetime(2020, 1, 1),
    default_args={"owner": "airflow_lesson"},
    template_searchpath=['/usr/local/airflow/sql']
)

start = DummyOperator(
    task_id='start',
    dag=dag
)

end = DummyOperator(
    task_id='end',
    dag=dag
)

generate_xcom = PythonOperator(
    task_id='generate_xcom',
    python_callable=fn_generate_xcom,
    provide_context=True,
    dag=dag
)

ex1 = PostgresOperator(
    task_id='template_fstring',
    sql=f'SELECT count(*) FROM {table};',
    postgres_conn_id='airflow_docker_db',
    dag=dag
)

ex2 = PostgresOperator(
    task_id='template_file',
    sql='template_file.sql',
    postgres_conn_id='airflow_docker_db',
    dag=dag
)

ex3 = PostgresOperator(
    task_id='template_in_file',
    sql='template_in_file.sql',
    postgres_conn_id='airflow_docker_db',
    params={"my_param": 'follow_me'},
    dag=dag
)

ex4 = PostgresOperator(
    task_id='xcom_in_sql',
    sql="SELECT {{ ti.xcom_pull(key='my_xcom', task_ids='generate_xcom') }};",
    postgres_conn_id='airflow_docker_db',
    dag=dag
)

ex5 = PostgresOperator(
    task_id='xcom_in_sql_file',
    sql='xcom_in_sql_file.sql',
    postgres_conn_id='airflow_docker_db',
    dag=dag
)

ex6 = PostgresOperator(
    task_id='xcom_in_fstring',
    sql=f"SELECT {{{{ ti.xcom_pull(key='my_xcom', task_ids='generate_xcom') }}}} AS {random.choice(['x','y'])}",
    postgres_conn_id='airflow_docker_db',
    dag=dag
)

start >> generate_xcom >> ex1 >> ex2 >> ex3 >> ex4 >> ex5 >> ex6 >> end
