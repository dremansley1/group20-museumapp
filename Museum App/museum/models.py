from datetime import datetime
from museum import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    password = db.Column(db.String(60), nullable=False)
   
    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"
        
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


class ArtPiece(db.Model):
    artworkID = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50),nullable=False)
    description = db.Column(db.String(120), nullable=False)
    date = db.Column(db.Date, nullable=False)
    picturePath = db.Column(db.String(30), nullable=False, default='defaultPic.jpg')
    audioPath = db.Column(db.String(30), nullable=False, default='defaultAudio.mp3')
    VideoPath = db.Column(db.String(30), nullable=False, default='defaultVideo.mp3')
    locationX = db.Column(db.Integer, nullable = False)
    locationY = db.Column(db.Integer, nullable = False)

    def __repr__(self):
        return f"ArtPiece('{self.title}', '{self.description}', '{self.date}', '{self.locationX}'), '{self.locationY}')"

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
