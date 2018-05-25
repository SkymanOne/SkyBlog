from flask import Flask

app = Flask(__name__)
app.env = 'development'
app.debug = True
app.testing = True
app.config.from_object('config')

from app import routing
