import sys
sys.path.insert(0, 'd:\\novel-1\\novel_sys')

from app import app, db
from models.BlogPost import BlogPost

with app.app_context():
    posts = BlogPost.query.all()
    for post in posts:
        print(f"ID: {post.post_id}")
        print(f"标题: {post.title}")
        print(f"图片URL: {post.image_url}")
        print(f"是否有图片: {'是' if post.image_url else '否'}")
        print("-" * 30)
