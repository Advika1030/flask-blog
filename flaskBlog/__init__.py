#__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate



app = Flask(__name__)
app.config['SECRET_KEY'] = 'ea68fc1240295f35914343452aab7ffb'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app) #creats sql alchemy database instance
migrate =  Migrate(app,db)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'  #in bootstrap its a blue information alert

from flaskBlog import routes