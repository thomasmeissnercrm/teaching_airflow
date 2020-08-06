from airflow.operators.dummy_operator import DummyOperator
from airflow.models import DAG, Variable, datetime


GENERAL_VAR = Variable.get('generate_tasks', deserialize_json=True)

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

end = DummyOperator(
    task_id='end',
    dag=dag
)

start >> [t1, t2, t3] >> end
