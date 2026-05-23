from datetime import datetime
from db import db

class CheckinSpot(db.Model):
    """打卡点模型"""
    __tablename__ = 'checkin_spot'
    
    spot_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(255))
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    image_url = db.Column(db.String(255))
    rating = db.Column(db.Float, default=0.0)
    checkin_count = db.Column(db.Integer, default=0)
    status = db.Column(db.SmallInteger, default=1)
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    def __repr__(self):
        return f'<CheckinSpot {self.name}>'