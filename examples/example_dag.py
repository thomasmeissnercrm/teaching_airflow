"""
Here you put information what your dag is doing and what data is processes (source and target)

Data_in: sources of data
Data_out: target place of data that you process
Depend_on: if pipeline is depending on other one to execute - write it!
@author: your full name
@team: your squad
@stakeholders: name of team/person
"""
from airflow.operators.dummy_operator import DummyOperator
from airflow.models import DAG
import datetime

# Dag declaration
dag = DAG(
    dag_id='example_dag',
    schedule_interval=None,
    start_date=datetime.datetime(2020, 1, 1),
    default_args={"owner": "example_owner"}
)

# Tasks declaration
start = DummyOperator(
    task_id='start_dag',
    dag=dag
)

end = DummyOperator(
    task_id='end_dag',
    dag=dag
)

# Declaration of relations between tasks
start >> end
