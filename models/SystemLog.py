import datetime
from db import db


class SystemLog(db.Model):

    __tablename__ = 'system_log'
    __table_args__ = {'extend_existing': True}

    log_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.admin_id'))
    operate_type = db.Column(db.String(30), nullable=False)
    operate_content = db.Column(db.String(255), nullable=False)
    operate_time = db.Column(db.DateTime, default=datetime.datetime.now)
    ip_address = db.Column(db.String(50))
