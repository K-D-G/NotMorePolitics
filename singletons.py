from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from constants import*

class FlaskApp:
    instance=None
    def __init__(self):
        FlaskApp.get()
    def get():
        if not FlaskApp.instance:
            FlaskApp.instance=Flask(NAME) #Main instance for the application
            FlaskApp.instance.config['WHOOSH_BASE']='database/search.db'
            #FlaskApp.instance.config['WHOOSH_BASE']='database/whoosh'
            FlaskApp.instance.secret_key=SECRET_KEY #For encryption etc
        return FlaskApp.instance

class Database:
    instance=None
    def __init__(self):
        Database.get()
    def get():
        if not Database.instance:
            FlaskApp.get().config["SQLALCHEMY_DATABASE_URI"]=DATABASE_PATH #Give the application information about the database (location)
            FlaskApp.get().config["SQLALCHEMY_TRACK_MODIFICATIONS"]=SQLALCHEMY_TRACK_MODIFICATIONS
            Database.instance=SQLAlchemy(FlaskApp.get())
        return Database.instance

class FlaskLogin:
    instance=None
    def __init__(self):
        FlaskLogin.get()
    def get():
        if not FlaskLogin.instance:
            FlaskLogin.instance=LoginManager()
            FlaskLogin.instance.init_app(FlaskApp.get())
        return FlaskLogin.instance

class FlaskPasswordHasher:
    instance=None
    def __init__(self):
        FlaskPasswordHasher.get()
    def get():
        if not FlaskPasswordHasher.instance:
            FlaskPasswordHasher.instance=Bcrypt(FlaskApp.get())
        return FlaskPasswordHasher.instance
