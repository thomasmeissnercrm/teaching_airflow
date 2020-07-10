from airflow.hooks.postgres_hook import PostgresHook
from contextlib import closing
import sys


class PostgresExtendedHook(PostgresHook):

    def __init__(self, conn_id, *args, **kwargs):
        self.conn_id = conn_id
        super(PostgresHook).__init__(*args, **kwargs)

    def get_pandas_df(self, sql, parameters=None, chunk_size=None):
        if sys.version_info[0] < 3:
            sql = sql.encode('utf-8')
        import pandas.io.sql as psql

        with closing(self.get_conn()) as conn:
            return psql.read_sql(sql, con=conn, chunksize=chunk_size, params=parameters)