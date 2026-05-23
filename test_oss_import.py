import sys
sys.path.insert(0, '.')

# 测试直接导入oss2
print("测试直接导入oss2...")
try:
    from oss2 import Auth, Bucket, exceptions, ObjectACL
    print("✓ oss2导入成功")
except ImportError as e:
    print("✗ oss2导入失败:", str(e))
    import traceback
    traceback.print_exc()

# 测试从oss_utils导入
print("\n测试从oss_utils导入...")
try:
    from utils.oss_utils import oss_manager, OSS_AVAILABLE
    print("OSS_AVAILABLE:", OSS_AVAILABLE)
except Exception as e:
    print("导入失败:", str(e))
    import traceback
    traceback.print_exc()
