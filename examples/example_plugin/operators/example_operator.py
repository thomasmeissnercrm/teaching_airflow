from airflow.operators import BaseOperator
import logging


class ExampleOperator(BaseOperator):
    """
    Here also short description what operator is doing.
    """
    def __init__(self, my_parameter, *args, **kwargs):
        self.my_parameter = my_parameter
        super(BaseOperator).__init__(*args, **kwargs)

    @staticmethod
    def additional_method(self):
        """
        Remember to put information what method is doing!
        :param self:
        :return:
        """
        logging.info('You can also put as many methods as needed. Also static one')

    def execute(self, context):
        """
        Ex. Method is add two strings to log.
        :param context:
        :return:
        """
        logging.info('Here is your code that will be executed by operator')
        logging.info('the execute method is obligatory to implement in operator!')

