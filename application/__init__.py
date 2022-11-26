
from flask import Flask

app = Flask(__name__)

app.config['SECRET_KEY'] = 'thisisasecret'

from application import routes