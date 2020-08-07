"""
This pipeline shows how generate task sequentially.

Data_in: None
Data_out: None
Depend_on: None
@author: Rafal Chmielewski
@team: Airflow Learning
@stakeholders: People who learns
"""
from airflow.operators.dummy_operator import DummyOperator
from airflow.models import DAG, datetime

dag = DAG(
    dag_id='sequential_generation_example',
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

middle_task = DummyOperator(
    task_id="middle_task",
    dag=dag
)

sequential_tasks = []
for s in range(0, 6):
    sequential_task = DummyOperator(
        task_id=f"sequential_task_{s}",
        dag=dag
    )

    sequential_tasks.append(sequential_task)
    if s == 0:
        middle_task >> sequential_tasks[s]
    else:
        sequential_tasks[s - 1] >> sequential_tasks[s]
        if s == 5: sequential_tasks[s] >> end

start >> middle_task