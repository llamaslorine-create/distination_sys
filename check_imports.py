import sys
import io

# 设置标准输出编码为UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("Python版本:", sys.version)
print("开始检查模块导入...")

try:
    print("\n1. 检查配置文件...")
    from config import *
    print("   [OK] config.py 导入成功")
except Exception as e:
    print(f"   [ERROR] config.py 导入失败: {e}")

try:
    print("\n2. 检查数据库模块...")
    from db import db
    print("   [OK] db.py 导入成功")
except Exception as e:
    print(f"   [ERROR] db.py 导入失败: {e}")

try:
    print("\n3. 检查模型模块...")
    from models.Admin import Admin
    from models.Role import Role
    from models.User import User
    from models.Novel import Novel
    from models.Category import Category
    from models.Comment import Comment
    from models.SystemLog import SystemLog
    from models.Carousel import Carousel
    from models.VisualConfig import VisualConfig
    print("   [OK] 所有模型模块导入成功")
except Exception as e:
    print(f"   [ERROR] 模型模块导入失败: {e}")

try:
    print("\n4. 检查视图模块...")
    from views.auth import bp as auth_bp
    from views.dashboard import bp as dashboard_bp
    from views.user import bp as user_bp
    from views.novel import bp as novel_bp
    from views.category import bp as category_bp
    from views.system import bp as system_bp
    from views.comment import bp as comment_bp
    from views.visual import bp as visual_bp
    print("   [OK] 所有视图模块导入成功")
except Exception as e:
    print(f"   [ERROR] 视图模块导入失败: {e}")

try:
    print("\n5. 检查工具模块...")
    from utils.decorators import *
    from utils.encryption import *
    from utils.file_upload import *
    from utils.visualization import *
    print("   [OK] 所有工具模块导入成功")
except Exception as e:
    print(f"   [ERROR] 工具模块导入失败: {e}")

try:
    print("\n6. 检查主应用...")
    from app import app
    print("   [OK] app.py 导入成功")
except Exception as e:
    print(f"   [ERROR] app.py 导入失败: {e}")

print("\n检查完成!")
