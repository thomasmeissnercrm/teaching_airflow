"""
This pipeline shows how work with queues.

Data_out: None
Depend_on: None
@author: Rafal Chmielewski
@team: Airflow Learning
@stakeholders: People who learns
"""

from airflow.operators.dummy_operator import DummyOperator
from airflow.models import DAG, datetime


dag = DAG(
    dag_id='queues_example',
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

t1 = DummyOperator(
    task_id='default_queue',
    queue='default',
    dag=dag
)

t2 = DummyOperator(
    task_id='default_queue2',
    dag=dag
)

t3 = DummyOperator(
    task_id='secret_queue',
    queue='secret',
    dag=dag
)

start >> [t1, t2, t3] >> end
