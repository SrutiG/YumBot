'''
Title
-----
__init__.py

Description
-----------
Create app module

'''

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import config

app = Flask(__name__)
app.secret_key="secretKey1"
app.config.from_pyfile("config.py")
db = SQLAlchemy(app)

from app import views, models