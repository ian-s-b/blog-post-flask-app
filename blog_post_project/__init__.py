from pathlib import Path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)

#CONFIGURATIONS
##Secret Key
# app.config['SECRET_KEY'] = 'some_secret_key0'

##Database
basedir = Path(__file__).parent.resolve()
print(basedir)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + str(Path(basedir, 'data.sqlite'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app,db)

##Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "users.login"

#BLUEPRINTS
##Imports
from blog_post_project.core.views import core
from blog_post_project.error_pages.handlers import error_pages
from blog_post_project.blog_posts.views import blog_posts
from blog_post_project.users.views import users

##Register blueprints
app.register_blueprint(core)
app.register_blueprint(users)
app.register_blueprint(blog_posts)
app.register_blueprint(error_pages)