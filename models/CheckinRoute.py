from datetime import datetime
from db import db

class CheckinRoute(db.Model):
    """打卡路线模型"""
    __tablename__ = 'checkin_route'
    
    route_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    cover_image = db.Column(db.String(255))
    status = db.Column(db.SmallInteger, default=1)
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    spots = db.relationship('RouteSpot', backref='route', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<CheckinRoute {self.name}>'

class RouteSpot(db.Model):
    """路线打卡点关联模型"""
    __tablename__ = 'route_spot'
    
    id = db.Column(db.Integer, primary_key=True)
    route_id = db.Column(db.Integer, db.ForeignKey('checkin_route.route_id'))
    spot_id = db.Column(db.Integer, db.ForeignKey('checkin_spot.spot_id'))
    order_num = db.Column(db.Integer, nullable=False)
    
    spot = db.relationship('CheckinSpot', backref='route_spots')
    
    def __repr__(self):
        return f'<RouteSpot {self.route_id}-{self.spot_id}>'