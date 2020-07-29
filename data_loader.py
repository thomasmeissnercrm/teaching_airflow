from sqlalchemy import create_engine
import pandas as pd
import os

# create list of files to import
table_list = []
print('Loading list of files to upload in db.')
for path, subdirs, files in os.walk(f'{os.getcwd()}/example_data'):
    for name in files:
        if name in ['.DS_Store']:
            pass
        data = os.path.join(path, name)
        data = data.split('/')
        system = data[-3]
        schema = data[-2]
        table = data[-1].split('.')[0]
        ext = data[-1].split('.')[-1]
        if system not in ['teaching_airflow', 'myapp'] and table not in ['readme']:
            table_list.append({
                "engine": system,
                "schema": schema,
                "table": table,
                "ext": ext
            })

print(f'Load done. Found {len(table_list)} files to upload.')
print('generating db engines')
psql = create_engine('postgresql://airflow:airflow@teaching_airflow_postgres_1:5432')
mysql = create_engine('mysql://root:airflow@teaching_airflow_mysql_1:3306/public')

# getting list of schema in mysql
mysql_schema = pd.read_sql('select SCHEMA_NAME AS "schema" from information_schema.SCHEMATA;', con=mysql)['schema'].to_list()
psql_schema = pd.read_sql('Select schema_name as schema from information_schema.schemata;', con=psql)['schema'].to_list()

print('Loading data into databases')

for element in table_list:
    df = pd.read_csv(f'{os.getcwd()}/example_data/{element["engine"]}/{element["schema"]}/{element["table"]}.{element["ext"]}')
    db_engine = psql if element['engine'] == 'psql' else mysql
    if element['engine'] == 'mysql':
        if element["schema"] not in mysql_schema:
            mysql.execute(f"create schema {element['schema']}; ")
            mysql.execute(f"GRANT ALL PRIVILEGES ON {element['schema']}.* TO 'airflow'@'%';")
            mysql_schema.append(element["schema"])
    else:
        if element["schema"] not in psql_schema:
            psql.execute(f"create schema {element['schema']}; ")
            psql_schema.append(element["schema"])

    df.to_sql(
        name=element['table'],
        schema=element['schema'],
        con=db_engine,
        if_exists='replace'
    )
    print(f'Loaded table {element["schema"]}.{element["table"]} into {element["engine"]}')

print('Load done.')
