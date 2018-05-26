from flask import Flask
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.env = 'development'
app.debug = True
app.testing = True
app.config.from_object('config')
bootstrap = Bootstrap(app)

from app import routing
