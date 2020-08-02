from airflow.operators.dummy_operator import DummyOperator
from airflow.models import DAG
import datetime

dag = DAG(
    dag_id='many_tasks_example',
    schedule_interval=None,
    start_date=datetime.datetime(2020, 1, 1),
    default_args={"owner": "learning_airflow"}
)
start = DummyOperator(
    task_id='start',
    dag=dag
)

end = DummyOperator(
    task_id='end',
    dag=dag
)

task_list = []
for i in range(0, 100):
    middle_task = DummyOperator(
        task_id=f'mid_task_a{i}',
        dag=dag
    )

    middle_task2 = DummyOperator(
        task_id=f'mid_task_b{i}',
        dag=dag
    )
    t1 = DummyOperator(
        task_id=f'task_{i}',
        dag=dag
    )
    t2 = DummyOperator(
        task_id=f'another_task_{i}',
        dag=dag
    )
    t3 = DummyOperator(
        task_id=f'other_task{i}',
        dag=dag
    )
    t4 = DummyOperator(
        task_id=f'next_task_{i}',
        dag=dag
    )
    task_list.append(start >> middle_task >> middle_task2 >> t1 >> [t2, t3] >> t4 >> end)


task_list
