from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__)
app.config['SECRET_KEY'] = 'c0e04f0579501166c995eee771611c872215a31099c5725b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://c1827663:aMPDZdgMm44KdfS@csmysql.cs.cf.ac.uk:3306/c1827663'
#e.g.c1234567:mypassword@csmysql.cs.cf.ac.uk:3306/c1234567

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)


from shop import routes
