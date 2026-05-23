import sys
sys.path.insert(0, 'd:\\novel-1\\novel_sys')

from flask import Flask, redirect, url_for
from flask_login import LoginManager
from flask_wtf import CSRFProtect

from config import *
from db import db

app = Flask(__name__)

app.config.from_object('config')

db.init_app(app)

csrf = CSRFProtect(app)

from utils.oss_utils import init_oss
init_oss(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.user_login'

app.jinja_env.globals['hasattr'] = hasattr

def media_url(value, default_dir=''):
    """渲染图片 URL，兼容历史数据：
    - 完整 http(s) URL（OSS 或外链）原样返回
    - 以 / 开头的本地路径（如 /static/uploads/xxx）原样返回
    - 裸文件名按 default_dir 拼接为本地 static 路径
    """
    if not value:
        return ''
    if value.startswith('http://') or value.startswith('https://'):
        return value
    if value.startswith('/'):
        return value
    prefix = default_dir.strip('/')
    name = value.rsplit('/', 1)[-1]
    if prefix:
        return f'/static/uploads/{prefix}/{name}'
    return f'/static/uploads/{name}'

app.jinja_env.globals['media_url'] = media_url

from models.Admin import Admin
from models.Role import Role
from models.User import User
from models.SystemLog import SystemLog
from models.CheckinSpot import CheckinSpot
from models.VisitReport import VisitReport
from models.Badge import Badge
from models.CheckinRoute import CheckinRoute, RouteSpot
from models.UserCheckin import UserCheckin, UserBadge
from models.BlogPost import BlogPost, BlogComment
from models.Announcement import Announcement

@login_manager.user_loader
def load_user(user_id):
    # session 里存的形如 "a:1" / "u:1"；兼容历史无前缀的字符串（按 admin 优先回退到旧逻辑）
    s = str(user_id)
    if s.startswith('u:'):
        try:
            uid = int(s[2:])
        except ValueError:
            return None
        user = User.query.get(uid)
        if user:
            user.is_admin = False
            return user
        return None
    if s.startswith('a:'):
        try:
            aid = int(s[2:])
        except ValueError:
            return None
        admin = Admin.query.get(aid)
        if admin:
            admin.is_admin = True
            return admin
        return None
    # 旧 session 没有前缀：清掉它，让用户重新登录（避免错配）
    return None
    return None

from views.auth import bp as auth_bp
from views.dashboard import bp as dashboard_bp
from views.user import bp as user_bp
from views.system import bp as system_bp
from views.checkin import bp as checkin_bp
from views.report import bp as report_bp
from views.badge import bp as badge_bp
from views.route import bp as route_bp
from views.map import bp as map_bp
from views.blog import bp as blog_bp
from views.manage import bp as manage_bp
from views.gallery import bp as gallery_bp

app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(system_bp)
app.register_blueprint(checkin_bp)
app.register_blueprint(report_bp)
app.register_blueprint(badge_bp)
app.register_blueprint(route_bp)
app.register_blueprint(map_bp)
app.register_blueprint(blog_bp)
app.register_blueprint(manage_bp)
app.register_blueprint(gallery_bp)

@app.route('/')
def index():
    return redirect(url_for('user.index'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
