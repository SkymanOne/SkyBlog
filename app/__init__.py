from flask import Flask
from flask_bootstrap import Bootstrap
from flask_misaka import Misaka
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from config import Config
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.env = 'development'
app.debug = True
app.testing = True
app.config.from_object(Config)
bootstrap = Bootstrap(app)
login = LoginManager(app)
login.login_view = 'login'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
ma = Marshmallow(app)

from app import routing, models
