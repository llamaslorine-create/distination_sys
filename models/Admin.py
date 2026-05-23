from datetime import datetime
from db import db

class Admin(db.Model):
    """管理员模型"""
    __tablename__ = 'admin'

    admin_id = db.Column(db.Integer, primary_key=True)
    admin_account = db.Column(db.String(50), nullable=False, unique=True)
    admin_password = db.Column(db.String(100), nullable=False)
    admin_name = db.Column(db.String(30), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.role_id'))
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    status = db.Column(db.SmallInteger, default=1)

    def get_id(self):
        return f"a:{self.admin_id}"

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return self.status == 1

    @property
    def is_anonymous(self):
        return False