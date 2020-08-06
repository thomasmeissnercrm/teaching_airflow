from airflow.operators.dummy_operator import DummyOperator
from airflow.models import DAG, datetime

dag = DAG(
    dag_id='debug_example',
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

start >> end >> start