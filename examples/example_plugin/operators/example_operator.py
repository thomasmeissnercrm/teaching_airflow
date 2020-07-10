from airflow.operators import BaseOperator
import logging


class MyOperator(BaseOperator):
    def __init__(self, my_parameter, *args, **kwargs):
        self.my_paramter = my_parameter
        super(BaseOperator).__init__(*args, **kwargs)

    def execute(self, context):
        logging.info('Here is your code that will be executed by operator')

