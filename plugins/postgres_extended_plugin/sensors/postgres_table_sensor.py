from airflow.sensors.base_sensor_operator import BaseSensorOperator
from airflow.models import apply_defaults
from airflow.hooks.postgres_hook import PostgresHook
import logging


class PostgresTableSensor(BaseSensorOperator):
    """
    Sensor is checking if table is able to query and let dag run further if that's possible.
    :param postgres_conn_id: str -> name of Airflow connection ID
    :param table: str -> name of table in database
    :param schema: str -> name of schema in database
    """

    @apply_defaults
    def __init__(self,
                 postgres_conn_id: str,
                 table: str,
                 schema: str,
                 *args,
                 **kwargs):
        self.postgres_conn_id = postgres_conn_id
        self.table = table
        self.schema = schema
        super().__init__(*args, **kwargs)

    def poke(self, context):
        """
        Main execution point. Function is trying to run select query against table. If that was possible
        return true
        :param context:
        :return: bool
        """

        try:
            logging.info(f'Trying to query table {self.schema}.{self.table}')
            psql_hook = PostgresHook(self.postgres_conn_id)
            _ = psql_hook.run(f"SELECT * FROM {self.schema}.{self.table} LIMIT 1;")
        except Exception as ex:
            logging.info(f'Cannot query table. Details: {ex}')
            return False

        return True
