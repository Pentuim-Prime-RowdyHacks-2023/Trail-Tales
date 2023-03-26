from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import getenv

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = mysql://