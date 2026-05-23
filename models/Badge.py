from datetime import datetime
from db import db

class Badge(db.Model):
    """徽章模型"""
    __tablename__ = 'badge'
    
    badge_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    icon_url = db.Column(db.String(255))
    condition_type = db.Column(db.String(50))
    condition_value = db.Column(db.Integer)
    status = db.Column(db.SmallInteger, default=1)
    create_time = db.Column(db.DateTime, default=datetime.now)
    
    user_badges = db.relationship('UserBadge', backref='badge', lazy='dynamic')
    
    def __repr__(self):
        return f'<Badge {self.name}>'