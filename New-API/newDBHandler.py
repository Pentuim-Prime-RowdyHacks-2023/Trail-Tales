from os import getenv
from dotenv import load_dotenv
from quart import g, Quart, websocket
from quart_db import QuartDB
import json

load_dotenv()

USER = getenv('USER')
PASSWORD = getenv('PASSWORD')
HOST = getenv('HOST')
DATABASE = getenv('DATABASE')

app = Quart(__name__)
db = QuartDB(app, url=f"mysql+pymysql://{ USER }:{ PASSWORD }@{ HOST }/{ DATABASE }")

# gotta make a function for fetch_data()
async def fetch_data(uid: str, table_name: str = '', tale_id: str = '') -> str:
    if table_name is None:
        # Return the entire row for the given uid
        query = 'SELECT * FROM Bio LEFT JOIN Tales ON Tales.UID = Bio.UID'
        result = await g.connection.query(query)
    else:
        if tale_id is None:
            # Return the data from the specified table for the given uid
            query = f'SELECT * FROM {table_name} WHERE UID = {uid}'
            result = await g.connection.query(query)
        else:
            query = f'SELECT * FROM Tales WHERE UID = {uid} AND TaleID = {tale_id}'
            result = await g.connection.query(query)

    return result

# POST Data
async def post_data(data: dict, table_name: str) -> str:
    # Get the column names from the data keys
    columns = ', '.join(data.keys())
    # Get the parameter placeholders for the data values
    placeholders = ', '.join(f"${i+1}" for i in range(len(data)))
    # Construct the SQL query
    query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
    # Execute the query with the data values as parameters
    result = await g.connection.execute(query, *data.values())

    return result

async def update_data(uid: str, data: dict, table_name: str) -> str:
     # Get the column names from the data keys
    columns = ', '.join(data.keys())
    # Get the parameter placeholders for the data values
    set_statement = ', '.join(f"{columns[i]} = {data[columns[i]]}" for i in range(len(data)))
    query = f'UPDATE {table_name} SET ({set_statement}) WHERE UID = {uid}'
    result = await g.connection.execute(query)
    return result
