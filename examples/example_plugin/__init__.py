"""
Here is important part.
We want to let airflow easy know what plugins are ready to use in dags durning execution.
In that case we need to 'register them'. This always happen in __init__ file of plugin folder.
"""
from airflow.plugins_manager import AirflowPlugin
from example_plugin.operators.example_operator import ExampleOperator
from example_plugin.hooks.example_hook import ExampleHook
from example_plugin.sensors.example_sensor import ExampleSensor


class ExamplePlugin(AirflowPlugin):
    name = "example_plugin"
    operators = [ExampleOperator]
    sensors = [ExampleSensor]
    hooks = [ExampleHook]
