from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.postgres_operator import PostgresOperator
from airflow.models import DAG, Variable, datetime


GENERAL_VAR = Variable.get('generate_tasks', deserialize_json=True)

dag = DAG(
    dag_id='generate_task_example',
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

for i in range(0, len(GENERAL_VAR['table_list'])):
    task_list.append(
        PostgresOperator(
            task_id = f'{GENERAL_VAR["table_list"][i]}_{i}',
            sql=f'SELECT count(*) from other.{GENERAL_VAR["table_list"][i]}',
            postgres_conn_id=GENERAL_VAR['psql_conn_id'],
            pool=GENERAL_VAR['pool'],
            dag=dag
        )
    )

start >> task_list >> end
