'''
Title
-----
__init__.py

Description
-----------
Create app module

'''

from flask import Flask

app = Flask(__name__)
app.secret_key="secretKey1"

from app import views