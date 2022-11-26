import requests
from flask import Flask
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///crypto.db'
app.config['SECRET_KEY'] = 'thisisasecret'
db = SQLAlchemy(app)
app.app_context().push()
    
from application import routes
from application import models