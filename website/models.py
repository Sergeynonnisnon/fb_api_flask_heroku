from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class RegisterBot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    FB_access_token = db.Column(db.String(1000))
    FB_id_groop = db.Column(db.String(20))
    creator_post_skip = db.Column(db.String(1000))
    chanelSlack = db.Column(db.String(100))
    api_bot_secret_Slack = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    Bot = db.relationship('RegisterBot')
