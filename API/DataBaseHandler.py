from os import getenv
from dotenv import load_dotenv
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
import pandas as pd
import json

load_dotenv()

USER = getenv('USER')
PASSWORD = getenv('PASSWORD')
HOST = getenv('HOST')
DATABASE = getenv('DATABASE')

connection_str: str = f'mysql+pymysql://{ USER }:{ PASSWORD }@{ HOST }/{ DATABASE }'

engine = create_engine(connection_str, pool_recycle=3600)

session: Session = Session(engine)

db = engine.connect()

def fetch_data( uid: str, table: str ) -> (Exception | pd.DataFrame):
    if uid is None: 
        return Exception('uid is not provided')
    if table is None:
        return Exception('table is not provided')
    return pd.read_sql_table(table, engine)

def post_data( uid: str, table: str, data ) -> (Exception | str):
    if uid is None:
        return Exception('uid is not provided')
    if table is None:
        return Exception('table is not provided')
    if data is None:
        return Exception('data is not provided')
    with session.begin():
        session.add(json.loads(data))
    return f'Successfully appended to {table}!'
