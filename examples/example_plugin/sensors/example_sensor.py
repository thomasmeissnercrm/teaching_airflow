from airflow.sensors.base_sensor_operator import BaseSensorOperator
import logging


class ExampleSensor(BaseSensorOperator):
    """
    Put here comment of how sensor is working and parameters that is using
    :param my_parameter str -> ex. connection id used in sensor
    """
    def __init__(self, my_parameter, *args, **kwargs):
        self.my_parameter = my_parameter
        super(BaseSensorOperator).__init__(*args, **kwargs)

    def poke(self, context):
        """
        Each method also should have comment of what happend inside
        :param context:
        :return:
        """
        logging.info('Sensors required poke method as it will be executed in pipeline')
        logging.info('depending on needed condition, its need to return True of False value')

        if self.my_parameter is True:
            return True
        else:
            return False
