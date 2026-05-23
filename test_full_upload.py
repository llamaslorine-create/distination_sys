import sys
sys.path.insert(0, '.')

from flask import Flask, request
from flask_login import LoginManager, UserMixin
from io import BytesIO

app = Flask(__name__)
app.config.from_object('config')

# 初始化登录管理器
login_manager = LoginManager()
login_manager.init_app(app)

# 创建模拟用户
class MockUser(UserMixin):
    def __init__(self):
        self.id = 1
        self.is_admin = True

@login_manager.user_loader
def load_user(user_id):
    return MockUser()

# 测试完整上传流程
with app.app_context():
    print("=== 测试博客图片上传流程 ===")
    print("USE_OSS配置:", app.config.get('USE_OSS'))
    print("OSS_ENDPOINT:", app.config.get('OSS_ENDPOINT'))
    print("OSS_BUCKET_NAME:", app.config.get('OSS_BUCKET_NAME'))
    
    from utils.oss_utils import oss_manager
    
    # 创建测试图片文件
    test_content = b'fake image content for testing'
    file_data = BytesIO(test_content)
    file_data.filename = 'test_blog_image.jpg'
    
    # 测试上传
    print("\n开始上传测试图片...")
    image_url, error = oss_manager.upload_file(file_data, 'blog_images/')
    
    if image_url:
        print(f"上传成功！")
        print(f"图片URL: {image_url}")
        
        if 'oss-cn-hangzhou' in image_url:
            print("✓ 图片已上传到阿里云OSS")
        else:
            print("✗ 图片仍上传到本地")
            
    else:
        print(f"上传失败: {error}")
