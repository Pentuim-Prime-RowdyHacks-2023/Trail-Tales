from azure.storage.fileshare import ShareServiceClient, ShareFileClient
from dotenv import load_dotenv
from os import getenv

load_dotenv()

connection_string: str = str(getenv('CONNECTION_STRING'))

service = ShareServiceClient.from_connection_string(conn_str=connection_string)

file_client = ShareFileClient.from_connection_string(conn_str=connection_string, share_name='audio', file_path="/.")

def upload_file(uid, file) -> str:
    

