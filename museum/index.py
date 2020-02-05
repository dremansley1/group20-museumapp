from flask import Flask, render_template, request
from pymysql import connect, cursors
from flask_sqlalchemy import SQLAlchemy
from museum import db

app = Flask(__name__, static_folder="static");
