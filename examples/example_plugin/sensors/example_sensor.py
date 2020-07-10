from airflow.sensors.base_sensor_operator import BaseSensorOperator
import logging


class ExampleSensor(BaseSensorOperator):
    def __init__(self, my_parameter, *args, **kwargs):
        self.my_parameter = my_parameter
        super(BaseSensorOperator).__init__(*args, **kwargs)

    def poke(self, context):
        logging.info('Sensors requaired poke method as it will be executed in pipeline')
        logging.info('depending on needed contidion, its need to return True of False value')

        if self.my_parameter is True:
            return True
        else:
            return False