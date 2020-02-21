from pymysql import connect, cursors
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request
from flask_login import LoginManager
from museum.config import database_info as dbinfo

app = Flask(__name__, static_folder="static");

app.config['SECRET_KEY'] = 'c0e04f0579501166c995eee771611c872215a31099c5725b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://c1827663:aMPDZdgMm44KdfS@csmysql.cs.cf.ac.uk:3306/c1827663'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

login_manager=LoginManager()
login_manager.init_app(app)
 
from museum import routes
