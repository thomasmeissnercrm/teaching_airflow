from airflow.operators import BaseOperator
from airflow.exceptions import AirflowException
from postgres_extended_plugin.hooks.postgres_extended_hook import PostgresExtendedHook
from airflow.contrib.hooks.sftp_hook import SFTPHook
import logging
from tempfile import TemporaryFile


class PostgresSftpOperator(BaseOperator):
    template_ext = ('.sql',)
    template_fields = ['sql']

    def __init__(self,
                 psql_conn_id: str,
                 sftp_conn_id: str,
                 sql: str,
                 file_desc: dict,
                 *args,
                 **kwargs):
        self.psql_conn_id = psql_conn_id,
        self.sftp_conn_id = sftp_conn_id,
        self.sql = sql
        self.file_desc = file_desc
        self.file_desc = self.validate_file_desc()
        super(BaseOperator).__init__(*args, **kwargs)

    def validate_file_desc(self):
        if 'name' in self.file_desc.keys() and 'format' in self.file_desc.keys():
            return {"name": self.file_desc['name'], "format": self.file_desc['format']}
        else:
            raise AirflowException('file_desc does not have required keys: name, format')

    def execute(self, context):
        logging.info(f'Preparing dataframe...')
        df = PostgresExtendedHook(self.psql_conn_id).get_pandas_df(sql=self.sql)
        logging.info('Writing data into temp file')
        with TemporaryFile() as f:
            if self.file_desc['format'].lower() == 'csv':
                df.to_csv(f, sep=';', quotechar='|')
            if self.file_desc['format'].lower() == 'parquet':
                df.to_parquet(f, engine='pyarrow')
            try:
                logging.info('Sending file to SFTP')
                sftp_connection = SFTPHook(self.sftp_conn_id).get_conn()
                sftp_connection.put(localpath=f.name,
                                    remotepath=f'/{self.file_desc["name"]}.{self.file_desc["format"]}')
            except Exception as ex:
                raise AirflowException(f'Could not put file on SFTP. Details {ex}')
