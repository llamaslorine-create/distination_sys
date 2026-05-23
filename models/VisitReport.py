from datetime import datetime
from db import db

class VisitReport(db.Model):
    """探店报告模型"""
    __tablename__ = 'visit_report'
    
    report_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    spot_id = db.Column(db.Integer, db.ForeignKey('checkin_spot.spot_id'))
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(255))
    status = db.Column(db.SmallInteger, default=1)
    create_time = db.Column(db.DateTime, default=datetime.now)
    
    spot = db.relationship('CheckinSpot', backref='reports')
    
    def __repr__(self):
        return f'<VisitReport {self.title}>'