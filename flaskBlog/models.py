#models.py

from datetime import datetime
from flaskBlog import db,login_manager
from flask_login import UserMixin
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), unique=True, nullable = False)
    email = db.Column(db.String(120), unique=True, nullable = False)
    image_file = db.Column(db.String(20), nullable = False, default='default.jpg')
    password = db.Column(db.String(60), nullable = False)
    posts = db.relationship('Post',backref='author',lazy=True)
    

    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.image_file}')"
    

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    rsvps = db.relationship('RSVP', backref='post', lazy=True, cascade='all, delete-orphan')
    time = db.Column(db.String(10), nullable=True)  # Optional time field
    place = db.Column(db.String(100), nullable=True)  # Optional place field
    date = db.Column(db.Date, nullable=True)  # Optional date field
    

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"




class RSVP(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

    # Define a relationship to the User model
    user = db.relationship('User', foreign_keys=[user_id], backref=db.backref('rsvps', lazy='dynamic'))
    
