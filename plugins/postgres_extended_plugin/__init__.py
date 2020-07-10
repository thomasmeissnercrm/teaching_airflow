from airflow.plugins_manager import AirflowPlugin
from postgres_extended_plugin.hooks.postgres_extended_hook import PostgresExtendedHook


class ExamplePlugin(AirflowPlugin):
    name = "postgres_extended_plugin"
    hooks = [PostgresExtendedHook]