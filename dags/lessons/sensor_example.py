"""
This pipeline example how sensors can be used.

Data_in:
    Postgres:
        - other.beers
Data_out: None
Depend_on: None
@author: Rafal Chmielewski
@team: Airflow Learning
@stakeholders: People who learns
"""
from postgres_extended_plugin.sensors.postgres_table_sensor import PostgresTableSensor
from airflow.operators.dummy_operator import DummyOperator
from airflow.models import DAG
import datetime


dag = DAG(
    dag_id='psql_sensor_example',
    schedule_interval=None,
    start_date=datetime.datetime(2020, 1, 1),
    default_args={"owner": "airflow_lesson"}
)

start = DummyOperator(
    task_id='start_dag',
    dag=dag
)

exising_table = PostgresTableSensor(
    task_id='exising_table',
    postgres_conn_id='airflow_docker_db',
    schema='other',
    table='beers',
    timeout=30,
    dag=dag
)

not_existing_table = PostgresTableSensor(
    task_id='not_exising_table',
    postgres_conn_id='airflow_docker_db',
    schema='other',
    table='beers2',
    timeout=30,
    dag=dag
)

can_run = DummyOperator(
    task_id='can_run',
    dag=dag
)

cannot_run = DummyOperator(
    task_id='cannot_run',
    dag=dag
)

end = DummyOperator(
    task_id='end_dag',
    dag=dag
)

start >> exising_table >> can_run >> end
start >> not_existing_table >> cannot_run >> end
