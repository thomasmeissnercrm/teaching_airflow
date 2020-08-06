from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import DAG, Variable, Pool, datetime
from airflow.settings import Session
import logging
import pandas as pd


def generate_init():
    psql_hook = PostgresHook('airflow_docker_db')
    eng = psql_hook.get_sqlalchemy_engine()
    df = pd.read_sql("select table_name from information_schema.tables where table_schema='other';",
                     con=eng)
    table_list = df['table_name'].tolist()
    init_data= {
        'psql_conn_id': 'airflow_docker_db',
        'table_list': table_list,
        'pool': 'generate_tasks'
    }
    try:
        Variable.set(key='generate_tasks', value=init_data, serialize_json=True)
    except Exception as ex:
        logging.info(f'Could not set global variable. Details: {ex}')

    try:
        pool = Pool()
        pool.slots = 1
        pool.description = 'How many tasks can run at once'
        pool.pool = 'generate_tasks'
        session = Session()
        session.add(pool)
        session.commit()
    except Exception as ex:
        logging.info(f'Could not set pool. Details: {ex}')


dag = DAG(
    dag_id='init_generate_tasks_example',
    schedule_interval=None,
    start_date=datetime(2020, 1, 1),
    default_args={"owner": "airflow_lesson"}
)
start = DummyOperator(
    task_id='start',
    dag=dag
)

init = PythonOperator(
    task_id='init_pipeline',
    python_callable=generate_init,
    dag=dag
)

end = DummyOperator(
    task_id='end',
    dag=dag
)

start >> init >> end
