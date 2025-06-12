from . import db
from datetime import datetime
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), index=True, unique=True, nullable=False)
    email = db.Column(db.String(100), index=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    user_type = db.Column(db.String(20), nullable=False, default='guest')

    # Relation to call user.comments & comment.posted_by
    comments = db.relationship('Comment', backref='posted_by')
    
    def __repr__(self):
        return f"User: '{self.username}'"

class Destination(db.Model):
    __tablename__ = 'destinations'

    id = db.Column(db.Integer, primary_key=True)
    city_name = db.Column(db.String(80), nullable=False)
    country_name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    image = db.Column(db.String(400), default='/static/img/default.png')
    exchange_rate = db.Column(db.Float, nullable=False)
    currency_code = db.Column(db.String(3), nullable=False)

	# Relation to call destination.comments & comment.destination
    comments = db.relationship('Comment', backref='destination')

    def __repr__(self):
        return f"Destination: '{self.city_name}, {self.country_name}'"

class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(400))
    posted_at = db.Column(db.DateTime, default=datetime.now())

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    destination_id = db.Column(db.Integer, db.ForeignKey('destinations.id'))

    def __repr__(self):
        return f"Comment: '{self.text}' posted by User #{self.user_id}"