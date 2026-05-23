import sys
sys.path.insert(0, 'd:\\novel-1\\novel_sys')

from app import app, db

with app.app_context():
    from sqlalchemy import text
    try:
        db.session.execute(text('ALTER TABLE blog_post ADD COLUMN image_url VARCHAR(500) NULL;'))
        db.session.commit()
        print('字段添加成功')
    except Exception as e:
        print(f'错误: {e}')
