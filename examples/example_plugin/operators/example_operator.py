from airflow.operators import BaseOperator
import logging


class ExampleOperator(BaseOperator):
    def __init__(self, my_parameter, *args, **kwargs):
        self.my_parameter = my_parameter
        super(BaseOperator).__init__(*args, **kwargs)

    @staticmethod
    def additional_method(self):
        logging.info('You can also put as many methods as needed. Also static one')

    def execute(self, context):
        logging.info('Here is your code that will be executed by operator')
        logging.info('the execute method is obligatory to implement in operator!')

