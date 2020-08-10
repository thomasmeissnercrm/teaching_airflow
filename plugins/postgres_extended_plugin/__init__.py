from airflow.plugins_manager import AirflowPlugin
from postgres_extended_plugin.hooks.postgres_extended_hook import PostgresExtendedHook
from postgres_extended_plugin.operators.postgres_ftp_operator import PostgresFtpOperator
from postgres_extended_plugin.sensors.postgres_table_sensor import PostgresTableSensor


class PostgresExtendedPlugin(AirflowPlugin):
    name = "postgres_extended_plugin"
    hooks = [PostgresExtendedHook]
    operators = [PostgresFtpOperator]
    sensors = [PostgresTableSensor]
