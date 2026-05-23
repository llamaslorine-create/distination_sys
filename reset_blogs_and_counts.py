"""一次性维护脚本：
1. 清空 blog_post + blog_comment（保留本地/OSS 图片文件不动）
2. 所有 checkin_spot 的 checkin_count 覆盖为 50-3000 之间的随机整数
"""
import sys, os, random

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from app import app
from db import db
from sqlalchemy import text


def main():
    with app.app_context():
        n_post = db.session.execute(text('SELECT COUNT(*) FROM blog_post')).scalar()
        n_comment = db.session.execute(text('SELECT COUNT(*) FROM blog_comment')).scalar()
        print(f'[BEFORE] blog_post={n_post}  blog_comment={n_comment}')

        db.session.execute(text('DELETE FROM blog_comment'))
        db.session.execute(text('DELETE FROM blog_post'))
        try:
            db.session.execute(text('ALTER TABLE blog_post AUTO_INCREMENT = 1'))
            db.session.execute(text('ALTER TABLE blog_comment AUTO_INCREMENT = 1'))
        except Exception as e:
            print(f'[NOTE] reset auto_increment skipped: {e}')

        spots = db.session.execute(text('SELECT spot_id, name FROM checkin_spot ORDER BY spot_id')).fetchall()
        updated = 0
        for spot_id, name in spots:
            cnt = random.randint(50, 3000)
            db.session.execute(
                text('UPDATE checkin_spot SET checkin_count = :c WHERE spot_id = :s'),
                {'c': cnt, 's': spot_id},
            )
            updated += 1

        db.session.commit()

        n_post = db.session.execute(text('SELECT COUNT(*) FROM blog_post')).scalar()
        n_comment = db.session.execute(text('SELECT COUNT(*) FROM blog_comment')).scalar()
        print(f'[AFTER ] blog_post={n_post}  blog_comment={n_comment}')

        rows = db.session.execute(text('SELECT spot_id, name, checkin_count FROM checkin_spot ORDER BY spot_id')).fetchall()
        print(f'[CHECKIN] {updated} 个打卡点已更新：')
        for r in rows:
            print(f'  [{r[0]:>3}] {r[1]:<30}  count={r[2]}')


if __name__ == '__main__':
    main()
