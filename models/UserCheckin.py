from datetime import datetime
from db import db

class UserCheckin(db.Model):
    """用户打卡记录模型"""
    __tablename__ = 'user_checkin'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    spot_id = db.Column(db.Integer, db.ForeignKey('checkin_spot.spot_id'))
    checkin_time = db.Column(db.DateTime, default=datetime.now)
    
    def __repr__(self):
        return f'<UserCheckin {self.user_id}-{self.spot_id}>'

class UserBadge(db.Model):
    """用户徽章获得记录模型"""
    __tablename__ = 'user_badge'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    badge_id = db.Column(db.Integer, db.ForeignKey('badge.badge_id'))
    obtain_time = db.Column(db.DateTime, default=datetime.now)
    
    def __repr__(self):
        return f'<UserBadge {self.user_id}-{self.badge_id}>'