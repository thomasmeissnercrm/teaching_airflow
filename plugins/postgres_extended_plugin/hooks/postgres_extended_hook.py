from airflow.hooks.postgres_hook import PostgresHook
from airflow.exceptions import AirflowException
import logging
import pandas as pd


class PostgresExtendedHook(PostgresHook):
    conn_name_attr = 'postgres_conn_id'
    default_conn_name = 'postgres_default'
    supports_autocommit = True

    def __init__(self, *args, **kwargs):
        super(PostgresExtendedHook, self).__init__(*args, **kwargs)
        if 'conn_name_attr' in kwargs and kwargs['conn_name_attr'] in kwargs:
            self.postgres_conn_id = kwargs[kwargs['conn_name_attr']]
            logging.debug(f"+++ Override postgres_conn_id with {self.postgres_conn_id}")

    def get_pandas_df(self, sql, parameters=None, chunk_size=None):
        """
        Method is returning pandas DF based on provided SQL query
        :param sql: str -> sql file or path to file
        :param parameters: dict -> paramters that will be used to template sql query
        :param chunk_size: how many records (maximum) each df should posses in return.
        :return:
        """
        logging.info(f"getting postgres engine: {self.get_sqlalchemy_engine()} with uri: {self.get_uri()}")

        try:
            df = pd.read_sql(sql, self.get_sqlalchemy_engine(), chunksize=chunk_size)
        except Exception as ex:
            raise AirflowException(f"Get pandas df from sql statement: {sql} has failed with exception : {ex}")
        return df
