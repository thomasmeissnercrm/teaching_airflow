from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.postgres_operator import PostgresOperator
from airflow.models import DAG, Variable, datetime


GENERAL_VAR = Variable.get('generate_tasks', deserialize_json=True)

dag = DAG(
    dag_id='many_tasks_example',
    schedule_interval=None,
    start_date=datetime(2020, 1, 1),
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

for i in enumerate(GENERAL_VAR['table_list']):
    task_list.append(
        PostgresOperator(
            sql=f'SELECT count(*) from other.{task_list[i]}',
            postgres_conn_id=GENERAL_VAR['postgress_conn_id'],
            pool=''
            dag=dag
        )
    )

star