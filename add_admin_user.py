import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import bcrypt
from app import app
from db import db
from models.Admin import Admin
from models.User import User
from models.Role import Role

def add_admin_and_user():
    with app.app_context():
        print("添加管理员和用户数据...")
        
        # 添加管理员角色
        if not Role.query.filter_by(role_id=1).first():
            role = Role(role_id=1, role_name='超级管理员', permissions='all')
            db.session.add(role)
            db.session.commit()
            print("管理员角色添加成功")
        
        # 添加管理员账号
        if not Admin.query.filter_by(admin_id=1).first():
            hashed_password = bcrypt.hashpw('admin123'.encode('utf-8'), bcrypt.gensalt())
            admin = Admin(
                admin_id=1,
                admin_account='admin',
                admin_name='超级管理员',
                admin_password=hashed_password.decode('utf-8'),
                role_id=1,
                status=1
            )
            db.session.add(admin)
            db.session.commit()
            print("管理员账号添加成功")
        
        # 添加测试用户
        if not User.query.filter_by(user_id=1).first():
            hashed_password = bcrypt.hashpw('123456'.encode('utf-8'), bcrypt.gensalt())
            user = User(
                user_id=1,
                username='testuser',
                password=hashed_password.decode('utf-8'),
                nickname='测试用户',
                email='test@example.com',
                status=1
            )
            db.session.add(user)
            db.session.commit()
            print("测试用户添加成功")
        
        print("\n管理员和用户数据添加完成！")
        print("管理员账号: admin / admin123")
        print("测试用户: testuser / 123456")

if __name__ == '__main__':
    add_admin_and_user()
