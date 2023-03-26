from os import getenv
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

USER = getenv('USER')
PASSWORD = getenv('PASSWORD')
HOST = getenv('HOST')
DATABASE = getenv('DATABASE')

connection_str: str = f'mysql+pymysql://{ USER }:{ PASSWORD }@{ HOST }/{ DATABASE }'

engine = create_engine(connection_str, pool_recycle=3600)

session: Session = Session(engine)

db = engine.connect()

def fetch_data( uid: str = '', table = '' ) -> (Exception | pd.DataFrame):
    if uid is None: 
        return Exception('uid is not provided')
    if table is None:
        return Exception('table is not provided')
    return pd.read_sql_table(table, engine)
