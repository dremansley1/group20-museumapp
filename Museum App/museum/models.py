from datetime import datetime
from museum import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class Vistor(UserMixin, db.Model):
    visitor_id = db.Column(db.Integer, primary_key=True)
    last_artwork_visited = db.Column(db.Integer, nullable=False)
    recommendation_type = db.Column(db.String(20), nullable =False)
    language = db.Column(db.String(20), nullable=False)


class Artist(db.Model):
	artist_id = db.Column(db.Integer, primary_key=True)
	artist_name = db.Column(db.String(30), nullable=False)
	wiki_link = db.Column(db.String(200), nullable=False)


class Room(db.Model):
	room_id = db.Column(db.Integer, primary_key=True)
	room_title = db.Column(db.String(20), nullable=False)
	floor_number = db.Column(db.Integer, nullable=False)

class ArtPiece(db.Model):
    artwork_id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey("Artist.artist_id") , nullable=False)
    room_id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(50),nullable=False)
    description = db.Column(db.String(120), nullable=False)
    date = db.Column(db.Date, nullable=False)
    picture_path = db.Column(db.String(30), nullable=False, default='defaultPic.jpg')
    audio_path = db.Column(db.String(30), nullable=False, default='defaultAudio.mp3')
    video_path = db.Column(db.String(30), nullable=False, default='defaultVideo.mp3')
    location_x = db.Column(db.Integer, nullable = False)
    location_y = db.Column(db.Integer, nullable = False)

    def __repr__(self):
        return f"ArtPiece('{self.title}', '{self.description}', '{self.date}', '{self.locationX}'), '{self.locationY}')"


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"user('{self.username}')"
        
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
