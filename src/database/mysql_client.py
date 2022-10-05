import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class MysqlClient():
    ACCOUNT = 'testUser'
    PASSWORD = 'password'
    DATABASE = 'testDB'
    DOMAIN = os.getenv("DB_HOST", "localhost")
    _instance = None

    @staticmethod
    def get_instance():
        if MysqlClient._instance is None:
            MysqlClient()
        return MysqlClient._instance

    def __init__(self):
        if MysqlClient._instance is not None:
            raise Exception('only one instance can exist')
        else:
            engine = create_engine(
                f"mysql+pymysql://{MysqlClient.ACCOUNT}:{MysqlClient.PASSWORD}@{MysqlClient.DOMAIN}/{MysqlClient.DATABASE}")
            session = sessionmaker(engine)
            MysqlClient._instance = session()
