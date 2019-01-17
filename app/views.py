from app import app
from flask import render_template, redirect, session, request, jsonify, url_for

'''
Default route
'''
@app.route('/')
def index():
    return render_template('index.html')