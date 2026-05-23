from flask import Flask
from sqlalchemy import text
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import SQLALCHEMY_DATABASE_URI

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

from db import db
db.init_app(app)

from models.CheckinSpot import CheckinSpot

with app.app_context():
    print("=== 数据库调试 ===\n")
    
    print("1. 检查checkin_spot表...")
    try:
        result = db.session.execute(text("SHOW TABLES LIKE 'checkin_spot'")).fetchone()
        if result:
            print("   ✓ checkin_spot表存在")
        else:
            print("   ✗ checkin_spot表不存在")
    except Exception as e:
        print(f"   ✗ 查询失败: {e}")
    
    print("\n2. 测试查询打卡点...")
    try:
        spots = CheckinSpot.query.all()
        print(f"   ✓ 查询成功，共 {len(spots)} 条记录")
        if spots:
            for spot in spots:
                print(f"     - {spot.name}")
    except Exception as e:
        print(f"   ✗ 查询失败: {e}")
        import traceback
        traceback.print_exc()