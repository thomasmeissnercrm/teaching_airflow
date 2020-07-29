"""
This pipeline is quering table and dump data from it into sftp

Data_in:
    Postgres:
        - other.netflix_titles
Data_out:
    SFTP:
        - generated_file.csv
        - generated_file.parquet
Depend_on: None
@author: Rafal Chmielewski
@team: Airflow Learning
@stakeholders: People who learns
"""
from postgres_extended_plugin.operators.postgres_sftp_operator import PostgresSftpOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.models import DAG
import datetime


dag = DAG(
    dag_id='psql_sftp_example',
    schedule_interval=None,
    start_date=datetime.datetime(2020, 1, 1),
    default_args={"owner": "airflow_lesson"}
)

start = DummyOperator(
    task_id='start_dag',
    dag=dag
)

generate_csv = PostgresSftpOperator(
    task_id='generate_csv',
    psql_conn_id='airflow_psql',
    sftp_conn_id='local_sftp',
    file_desc={
        "name": "generated_file",
        "format": "csv"
    },
    sql='SELECT * FROM other.netflix_titles;',
    dag=dag
)

generate_parquet = PostgresSftpOperator(
    task_id='generate_parquet',
    psql_conn_id='airflow_psql',
    sftp_conn_id='local_sftp',
    file_desc={
        "name": "generated_file",
        "format": "parquet"
    },
    sql='SELECT * FROM other.netflix_titles;',
    dag=dag
)

end = DummyOperator(
    task_id='end_dag',
    dag=dag
)

start >> [generate_csv, generate_parquet] >> end
