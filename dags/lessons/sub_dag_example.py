"""
This pipeline shows how sub dags are created.

Data_in: None
Data_out: None
Depend_on: None
@author: Rafal Chmielewski
@team: Airflow Learning
@stakeholders: People who learns
"""
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.subdag_operator import SubDagOperator
from airflow.models import DAG, datetime


def prepare_sub_dag(parent_dag, child_dag):
    """
    Preparing sub dag based on parent
    :param parent_dag:
    :param child_dag:
    :return:
    """
    sub_dag = DAG(
        dag_id=f'{parent_dag}.{child_dag}',
        start_date=datetime(2020, 1, 1),
        schedule_interval=None,
    )

    t1 = DummyOperator(
        task_id=f'sub_dag_task1',
        dag=sub_dag,
    )
    t2 = DummyOperator(
        task_id=f'sub_dag_task2',
        dag=sub_dag,
    )
    t3 = DummyOperator(
        task_id=f'sub_dag_task3',
        dag=sub_dag,
    )
    t4 = DummyOperator(
        task_id=f'sub_dag_task4',
        dag=sub_dag,
    )
    t1 >> [t2, t3] >> t4
    return sub_dag


dag = DAG(
    dag_id='sub_dag_example',
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

r_task = DummyOperator(
    task_id=f'some_task',
    dag=dag
)
r_task_2 = DummyOperator(
    task_id=f'another_task',
    dag=dag
)

for i in range(0, 15):
    sub_dags = SubDagOperator(
        task_id=f'do_sub_dags_{i}',
        subdag=prepare_sub_dag(dag.dag_id, child_dag=f'do_sub_dags_{i}'),
        dag=dag
    )
    r_task_2 >> sub_dags >> end

start >> r_task >> r_task_2
