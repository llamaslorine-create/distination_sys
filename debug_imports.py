import sys
import traceback

def test_import(module_name):
    try:
        __import__(module_name)
        print(f"✓ 成功导入: {module_name}")
        return True
    except Exception as e:
        print(f"✗ 导入失败 {module_name}: {e}")
        traceback.print_exc()
        return False

print("开始测试导入...")

modules = [
    'flask',
    'flask_login',
    'flask_sqlalchemy',
    'flask_wtf',
    'bcrypt',
    'pymysql'
]

for module in modules:
    test_import(module)

print("\n测试模型导入...")
model_modules = [
    'models.User',
    'models.Admin',
    'models.CheckinSpot',
    'models.CheckinRoute',
    'models.VisitReport',
    'models.Badge',
    'models.UserCheckin',
    'models.BlogPost',
    'models.Announcement',
    'models.Role',
    'models.SystemLog'
]

sys.path.insert(0, 'd:\\novel-1\\novel_sys')

for module in model_modules:
    test_import(module)

print("\n测试完成")
