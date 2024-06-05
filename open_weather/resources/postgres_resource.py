from dagster import ConfigurableResource
from sqlalchemy import create_engine

class PostgresResource(ConfigurableResource):
    host: str
    dbname: str
    user: str
    password: str
    port: str

    def get_engine(self):
        """
        Returns a sqlalchemy engine.
        
        :param host: The host address of the PostgreSQL server
        :param dbname: The name of the database
        :param user: The username to connect to the database
        :param password: The password to connect to the database
        :param port: The port number (default is 5432)
        :return: A psycopg2 connection object
        """
        return create_engine(f'postgresql+psycopg2://{self.user}:{self.password}@{self.host}:{self.port}/{self.dbname}')