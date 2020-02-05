from pymysql import connect, cursors
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request
from flask_login import LoginManager
from museum.config import database_info as dbinfo

app.config['SECRET_KEY'] = '57d7df7fb77d95d9a33127e289febe5bcc9b4f85cd70dec3'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://' + dbinfo["username"] + ':' + dbinfo["password"] + '@' + dbinfo['host'] + dbinfo["username"] + ''

db = SQLAlchemy(app)
login_manager=LoginManager()
login_manager.init_app(app)
from museum import routes
