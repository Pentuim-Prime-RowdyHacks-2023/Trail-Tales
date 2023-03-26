from os import getenv
from dotenv import load_dotenv
from sqlalchemy import create_engine, select, insert, update, values, Table, MetaData
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

def fetch_data( uid: str, table: str ) -> (Exception | str):
    if uid is None: 
        return Exception('uid is not provided')
    if table is None:
        return Exception('table is not provided')
    
    Table_instance: Table = Table(table, MetaData())

    data = session.query(select(Table_instance).where(Table_instance.c.uid == uid))

    return json.dumps(data)

def fetch_row( uid: str, table: str, postid: str ) -> (Exception | str):
    if uid is None: 
        return Exception('uid is not provided')
    if table is None:
        return Exception('table is not provided')
    if postid is None:
        return Exception('postid is not provided')
    
    Table_instance: Table = Table(table, MetaData())
    
    data = session.query(select(Table_instance).where((Table_instance.c.uid == uid) & (Table_instance.c.postid == postid)))

    return json.dumps(data)

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

def update_table( uid: str, table: str, postid: str , data: dict ) -> (Exception | str):
    if uid is None:
        return Exception('uid is not provided')
    if table is None:
        return Exception('table is not provided')
    if data is None:
        return Exception('data is not provided')
    
    Table_instance = Table(table, MetaData())

    with session.begin():
        if postid is not None:
            session.execute(update(Table_instance).where((Table_instance.c.uid == uid) & (Table_instance.c.postid == postid)).values(data))
        else:
            session.execute(update(Table_instance).where((Table_instance.c.uid == uid)).values(data))
    
    return fetch_row(uid, table, postid)
