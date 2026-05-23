import sys
sys.path.insert(0, '.')

from flask import Flask
from io import BytesIO

app = Flask(__name__)
app.config.from_object('config')

with app.app_context():
    print("=== 调试OSS上传 ===")
    print("USE_OSS:", app.config.get('USE_OSS'))
    
    from utils.oss_utils import oss_manager, OSS_AVAILABLE
    
    print("OSS_AVAILABLE:", OSS_AVAILABLE)
    
    # 手动初始化OSS
    print("\n初始化OSS连接...")
    try:
        oss_manager._init_bucket()
        print("初始化成功")
        print("bucket对象:", oss_manager.bucket)
    except Exception as e:
        print("初始化失败:", str(e))
        import traceback
        traceback.print_exc()
    
    # 测试上传
    if oss_manager.bucket:
        print("\n尝试上传到OSS...")
        test_content = b'test content'
        try:
            headers = {'x-oss-object-acl': 'public-read'}
            result = oss_manager.bucket.put_object('test_debug.txt', test_content, headers=headers)
            print("上传结果状态码:", result.status)
            if result.status == 200:
                print("OSS上传成功！")
            else:
                print("OSS上传失败，状态码:", result.status)
        except Exception as e:
            print("OSS上传异常:", str(e))
            import traceback
            traceback.print_exc()
    else:
        print("bucket对象为空，无法上传到OSS")
