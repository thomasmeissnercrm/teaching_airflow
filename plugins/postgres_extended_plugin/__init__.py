from airflow.plugins_manager import AirflowPlugin
from postgres_extended_plugin.hooks.postgres_extended_hook import PostgresExtendedHook
from postgres_extended_plugin.operators.postgres_sftp_operator import PostgresSftpOperator


class ExamplePlugin(AirflowPlugin):
    name = "postgres_extended_plugin"
    hooks = [PostgresExtendedHook]
    operators = [PostgresSftpOperator]
