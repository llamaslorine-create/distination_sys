import sys
import traceback

sys.path.insert(0, 'd:\\novel-1\\novel_sys')

print("步骤1: 导入基本模块...")
try:
    from flask import Flask, redirect, url_for
    from flask_login import LoginManager
    from flask_wtf import CSRFProtect
    print("✓ 基本模块导入成功")
except Exception as e:
    print(f"✗ 基本模块导入失败: {e}")
    traceback.print_exc()
    exit(1)

print("\n步骤2: 导入配置和数据库...")
try:
    from config import *
    from db import db
    print("✓ 配置和数据库导入成功")
except Exception as e:
    print(f"✗ 配置和数据库导入失败: {e}")
    traceback.print_exc()
    exit(1)

print("\n步骤3: 创建应用实例...")
try:
    app = Flask(__name__)
    app.config.from_object('config')
    print("✓ 应用实例创建成功")
except Exception as e:
    print(f"✗ 应用实例创建失败: {e}")
    traceback.print_exc()
    exit(1)

print("\n步骤4: 初始化数据库...")
try:
    db.init_app(app)
    print("✓ 数据库初始化成功")
except Exception as e:
    print(f"✗ 数据库初始化失败: {e}")
    traceback.print_exc()
    exit(1)

print("\n步骤5: 初始化CSRF保护...")
try:
    csrf = CSRFProtect(app)
    print("✓ CSRF保护初始化成功")
except Exception as e:
    print(f"✗ CSRF保护初始化失败: {e}")
    traceback.print_exc()
    exit(1)

print("\n步骤6: 初始化登录管理器...")
try:
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.user_login'
    print("✓ 登录管理器初始化成功")
except Exception as e:
    print(f"✗ 登录管理器初始化失败: {e}")
    traceback.print_exc()
    exit(1)

print("\n步骤7: 导入模型...")
models = ['Admin', 'Role', 'User', 'SystemLog', 'CheckinSpot', 'VisitReport', 'Badge', 'CheckinRoute', 'RouteSpot', 'UserCheckin', 'UserBadge', 'BlogPost', 'BlogComment', 'Announcement']
for model in models:
    try:
        exec(f"from models.{model} import {model}")
        print(f"✓ 导入 {model} 成功")
    except Exception as e:
        print(f"✗ 导入 {model} 失败: {e}")
        traceback.print_exc()

print("\n步骤8: 设置用户加载器...")
try:
    @login_manager.user_loader
    def load_user(user_id):
        from models.Admin import Admin
        from models.User import User
        admin = Admin.query.get(int(user_id))
        if admin:
            admin.is_admin = True
            return admin
        user = User.query.get(int(user_id))
        if user:
            user.is_admin = False
            return user
        return None
    print("✓ 用户加载器设置成功")
except Exception as e:
    print(f"✗ 用户加载器设置失败: {e}")
    traceback.print_exc()
    exit(1)

print("\n步骤9: 导入并注册蓝图...")
blueprints = [
    ('views.auth', 'auth_bp'),
    ('views.dashboard', 'dashboard_bp'),
    ('views.user', 'user_bp'),
    ('views.system', 'system_bp'),
    ('views.checkin', 'checkin_bp'),
    ('views.report', 'report_bp'),
    ('views.badge', 'badge_bp'),
    ('views.route', 'route_bp'),
    ('views.map', 'map_bp'),
    ('views.blog', 'blog_bp'),
    ('views.manage', 'manage_bp')
]

for module, var_name in blueprints:
    try:
        exec(f"from {module} import bp as {var_name}")
        exec(f"app.register_blueprint({var_name})")
        print(f"✓ 注册 {module} 成功")
    except Exception as e:
        print(f"✗ 注册 {module} 失败: {e}")
        traceback.print_exc()

print("\n步骤10: 设置首页路由...")
try:
    @app.route('/')
    def index():
        return redirect(url_for('user.index'))
    print("✓ 首页路由设置成功")
except Exception as e:
    print(f"✗ 首页路由设置失败: {e}")
    traceback.print_exc()
    exit(1)

print("\n所有步骤完成！尝试启动应用...")
try:
    app.run(debug=True, port=5000)
except Exception as e:
    print(f"✗ 启动失败: {e}")
    traceback.print_exc()
    exit(1)
