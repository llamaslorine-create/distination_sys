import datetime
from db import db


class Role(db.Model):

    __tablename__ = 'role'

    role_id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(30), nullable=False)
    permissions = db.Column(db.String(255))
    remark = db.Column(db.String(100))
    create_time = db.Column(db.DateTime, default=datetime.datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
