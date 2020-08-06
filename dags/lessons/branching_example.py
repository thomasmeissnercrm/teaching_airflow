"""
This pipeline example how branching operator works.

Data_in: None
Data_out: None
Depend_on: None
@author: Rafal Chmielewski
@team: Airflow Learning
@stakeholders: People who learns
"""
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import BranchPythonOperator
from airflow.models import DAG, datetime
from random import choice


def make_choice():
    """
    Function is choosing random path for run
    :return:
    """
    options = ['task_1', 'task2', 'task_3']
    return choice(options)


dag = DAG(
    dag_id='branching_example',
    schedule_interval=None,
    start_date=datetime(2020, 1, 1),
    default_args={"owner": "airflow_lesson"}
)

start = DummyOperator(
    task_id='start',
    dag=dag
)

do_choice = BranchPythonOperator(
    task_id='do_choice',
    python_callable=make_choice,
    dag=dag
)

t1 = DummyOperator(
    task_id='task_1',
    dag=dag
)

t2 = DummyOperator(
    task_id='task_2',
    dag=dag
)

t3 = DummyOperator(
    task_id='task_3',
    dag=dag
)

t4 = DummyOperator(
    task_id='task_4',
    dag=dag
)

t5 = DummyOperator(
    task_id='task_5',
    dag=dag
)

t6 = DummyOperator(
    task_id='task_6',
    dag=dag
)

start >> do_choice
do_choice >> t1
do_choice >> t2
do_choice >> t3
t1 >> t4
t2 >> t5
t3 >> t6