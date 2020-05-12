from datetime import datetime

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(UserMixin, db.Model):
    id = db.Column(db.String(32), primary_key=True)
    username = db.Column(db.String(128), index=True, unique=True, nullable=False)
    email = db.Column(db.String(128), index=True, unique=True, nullable=False)
    is_authorized = db.Column(db.Integer, default=0, nullable=False)
    created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)


class OAuth(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(32), db.ForeignKey(User.id), nullable=False)
    token = db.Column(db.String(1024), nullable=False)
    access_token = db.Column(db.String(256), nullable=False)
    expires_in = db.Column(db.DateTime, nullable=False)
    provider = db.Column(db.String(10), default="google", nullable=False)
    expired = db.Column(db.Integer, default=0, nullable=False)
    created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    user = db.relationship(User)
