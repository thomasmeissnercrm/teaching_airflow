from airflow.hooks.postgres_hook import PostgresHook
from contextlib import closing
import sys


class PostgresExtendedHook(PostgresHook):

    def __init__(self, conn_id, *args, **kwargs):
        """
        Hook is responsible for interacting with PostgreSql database.
        :param conn_id: str -> Connection ID registered in airflow
        :param args:
        :param kwargs:
        """
        self.conn_id = conn_id
        super(PostgresHook).__init__(*args, **kwargs)

    def get_pandas_df(self, sql, parameters=None, chunk_size=None):
        """
        Method is returning pandas DF based on provided SQL query
        :param sql: str -> sql file or path to file
        :param parameters: dict -> paramters that will be used to template sql query
        :param chunk_size: how many records (maximum) each df should posses in return.
        :return:
        """
        if sys.version_info[0] < 3:
            sql = sql.encode('utf-8')
        import pandas.io.sql as psql

        with closing(self.get_conn()) as conn:
            return psql.read_sql(sql, con=conn, chunksize=chunk_size, params=parameters)
