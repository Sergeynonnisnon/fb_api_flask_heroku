from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class RegisterBot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    FB_access_token = db.Column(db.String(1000))
    FB_id_groop = db.Column(db.String(1000))
    FB_app_secret = db.Column(db.String(1000))
    FB_app_id = db.Column(db.String(1000))
    creator_post_skip = db.Column(db.String(1000))
    chanelSlack = db.Column(db.String(1000))
    api_bot_secret_Slack = db.Column(db.String(1000))

    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('RegisterBot')
