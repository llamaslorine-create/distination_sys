from datetime import datetime
from db import db

class BlogPost(db.Model):
    """旅游博文模型"""
    __tablename__ = 'blog_post'
    
    post_id = db.Column(db.Integer, primary_key=True)
    author_name = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(500))
    status = db.Column(db.SmallInteger, default=1)
    view_count = db.Column(db.Integer, default=0)
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    comments = db.relationship('BlogComment', backref='post', cascade='all, delete-orphan', order_by='BlogComment.create_time')
    
    def __repr__(self):
        return f'<BlogPost {self.title}>'

class BlogComment(db.Model):
    """博文评论模型"""
    __tablename__ = 'blog_comment'
    
    comment_id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('blog_post.post_id'))
    parent_id = db.Column(db.Integer, db.ForeignKey('blog_comment.comment_id'))
    author_name = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=False)
    status = db.Column(db.SmallInteger, default=1)
    create_time = db.Column(db.DateTime, default=datetime.now)
    
    replies = db.relationship('BlogComment', backref=db.backref('parent', remote_side=[comment_id]))
    
    def __repr__(self):
        return f'<BlogComment {self.comment_id}>'