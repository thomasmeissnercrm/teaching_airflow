SELECT {{ ti.xcom_pull(key='my_xcom', task_ids='generate_xcom') }} as field;
