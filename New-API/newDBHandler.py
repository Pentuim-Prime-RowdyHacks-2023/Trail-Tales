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
db = QuartDB(app, url="mysql+pymysql://{ USER }:{ PASSWORD }@{ HOST }/{ DATABASE }")

# gotta make a function for fetch_data()
async def fetch_data(uid: str, table_name: str = None):
    if table_name is None:
        # Return the entire row for the given uid
        query = "SELECT * FROM my_table WHERE uid = $1"
        result = await g.connection.fetchrow(query, uid)
    else:
        # Return the data from the specified table for the given uid
        query = f"SELECT {table_name} FROM my_table WHERE uid = $1"
        result = await g.connection.fetchval(query, uid)

    return result
# gotta make a 
async def post_data(data: dict, table_name: str):
    # Get the column names from the data keys
    columns = ', '.join(data.keys())
    # Get the parameter placeholders for the data values
    placeholders = ', '.join(f"${i+1}" for i in range(len(data)))
    # Construct the SQL query
    query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
    # Execute the query with the data values as parameters
    await g.connection.execute(query, *data.values())