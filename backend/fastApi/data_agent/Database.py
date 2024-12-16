from sqlalchemy import create_engine, inspect

from fastApi.data_agent.Config import Config


class Database:
    """Handles database connections and setup."""
    def __init__(self, config: Config):
        self.db_host = config.get('DATABASE', 'host')
        self.db_user = config.get('DATABASE', 'user')
        self.db_password = config.get('DATABASE', 'password')
        self.db_port = config.get('DATABASE', 'port')
        self.db_name = config.get('DATABASE', 'db_name')
        self.engine = self.create_engine()

    def create_engine(self):
        """Create and return a SQLAlchemy engine."""
        return create_engine(
            f'mysql+pymysql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}')

    def get_tables(self):
        """Get all table names from the database."""
        inspector = inspect(self.engine)
        return inspector.get_table_names()