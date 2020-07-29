from airflow.operators import BaseOperator
from airflow.exceptions import AirflowException
from postgres_extended_plugin.hooks.postgres_extended_hook import PostgresExtendedHook
from airflow.contrib.hooks.ftp_hook import FTPHook
import logging
from tempfile import NamedTemporaryFile


class PostgresFtpOperator(BaseOperator):
    """
    Operator is responsible for dumping data from postgres into file on sftp server.

    :param postgres_conn_id -> str - connection id for Postgres DB in Airflow
    :param sftp_conn_id -> str - connection id for SFTP in Airflow
    :param sql -> str - sql query or path to file with it
    :param file_desc -> dict - Python dictionary that include name and format of file ex.
            file_desc = {
            "name": "my_file_name",
            "format" "csv" or "parquet"
            }
    """
    template_fields = ('sql',)
    template_ext = ('.sql', )
    ui_color = '#ffad33'

    def __init__(self,
                 postgres_conn_id: str,
                 sftp_conn_id: str,
                 sql: str,
                 file_desc: dict,
                 *args,
                 **kwargs):
        self.sql = sql
        self.postgres_conn_id = postgres_conn_id
        self.sftp_conn_id = sftp_conn_id
        self.file_desc = file_desc
        super().__init__(*args, **kwargs)

    def validate_file_desc(self):
        """
        Function is validating if file_desc dictionary contain required data. If not it raise AirflowException
        :return: dict
        """
        if 'name' not in self.file_desc.keys() or 'format' not in self.file_desc.keys():
            raise AirflowException('file_desc does not have required keys: name, format')
        elif self.file_desc['format'].lower() not in ['csv', 'parquet']:
            raise AirflowException('file_desc have incorrect format type: csv, parquet')
        else:
            return {"name": self.file_desc['name'], "format": self.file_desc['format']}

    def execute(self, context):
        """
        Main execution point. Steps that are done
            1) connecting to Postgres DB
            2) queering DB and pull data into pandas dataframe
            3) dump data from dataframe into file
            4) send file on SFTP server.
        :param context:
        :return: none
        """
        logging.info(f'Preparing dataframe...')
        psql_hook = PostgresExtendedHook().get_hook(self.postgres_conn_id)
        df = psql_hook.get_pandas_df(sql=self.sql)
        logging.info('Writing data into temp file')
        with NamedTemporaryFile() as f:
            if self.file_desc['format'].lower() == 'csv':
                df.to_csv(f.name, sep=';', quotechar='|')
            if self.file_desc['format'].lower() == 'parquet':
                df.to_parquet(f.name, engine='pyarrow')
            try:
                logging.info('Sending file to FTP')
                print(self.sftp_conn_id)
                ftp_hook = FTPHook(ftp_conn_id=self.sftp_conn_id)
                conn = ftp_hook.get_conn()
                f.flush()
                conn.set_pasv(False)
                conn.storbinary(f'STOR {self.file_desc["name"]}.{self.file_desc["format"]}', open(f.name, 'rb'), 1)

            except Exception as ex:
                raise AirflowException(f'Could not put file on SFTP. Details {ex}')
