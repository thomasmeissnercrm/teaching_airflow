from airflow.hooks.base_hook import BaseHook
import logging


class ExampleHook(BaseHook):
    """
    Here is comment of how your hook is working
    :param
    my_parameter: str -> information what should be inside parameter ex. connection_id etc.
    """
    def __init__(self, my_parameter, *args, **kwargs):
        self.my_parameter = my_parameter
        super(BaseHook).__init__(*args, **kwargs)

    def some_mehtod(self):
        """
        Here explanation what method does
        :return:
        """
        logging.info("I'm doing something!")
