import datetime
from db import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = 'user'

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    nickname = db.Column(db.String(50))
    email = db.Column(db.String(100))
    avatar_url = db.Column(db.String(255))
    status = db.Column(db.SmallInteger,default=1)
    create_time = db.Column(db.DateTime, default=datetime.datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.datetime.now)
    
    def get_id(self):
        return f"u:{self.user_id}"