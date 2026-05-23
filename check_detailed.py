import sys
import io

# 设置标准输出编码为UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("Python版本:", sys.version)
print("开始详细检查模块导入...")

# 检查各个依赖包
print("\n=== 检查依赖包 ===")
packages = ['flask', 'flask_login', 'flask_sqlalchemy', 'flask_wtf', 
            'bcrypt', 'pymysql', 'requests', 'matplotlib', 'seaborn', 'pandas']

for package in packages:
    try:
        __import__(package)
        print(f"  [OK] {package}")
    except ImportError:
        print(f"  [ERROR] {package} - 未安装")

print("\n=== 检查项目模块 ===")

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
    print("   [OK] 基础工具模块导入成功")
except Exception as e:
    print(f"   [ERROR] 基础工具模块导入失败: {e}")

try:
    print("\n6. 检查可视化模块...")
    from utils.visualization import *
    print("   [OK] 可视化模块导入成功")
except Exception as e:
    print(f"   [ERROR] 可视化模块导入失败: {e}")
    print("   提示: 可视化功能需要 matplotlib, seaborn, pandas 包")

try:
    print("\n7. 检查AI模块...")
    from utils.ai import *
    print("   [OK] AI模块导入成功")
except Exception as e:
    print(f"   [ERROR] AI模块导入失败: {e}")

try:
    print("\n8. 检查主应用...")
    from app import app
    print("   [OK] app.py 导入成功")
except Exception as e:
    print(f"   [ERROR] app.py 导入失败: {e}")

print("\n=== 检查完成 ===")
print("\n如果可视化模块导入失败，请运行以下命令安装依赖:")
print("  pip install matplotlib seaborn pandas")
print("\n或者使用 requirements.txt:")
print("  pip install -r requirements.txt")
