#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
阿里云OSS图片存储服务
注意：此文件提供了OSS图片存储的框架
实际使用时需要安装依赖：pip install oss2
pip install aliyun-python-sdk-core
pip install aliyun-python-sdk-oss
"""

import oss2
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime
import uuid
import config


class OSSService:
    """阿里云OSS服务类"""
    
    def __init__(self):
        """初始化OSS服务"""
        # OSS配置 - 请在config.py中配置以下参数：
        # OSS_ACCESS_KEY_ID = 'your-access-key-id'
        # OSS_ACCESS_KEY_SECRET = 'your-access-key-secret'
        # OSS_ENDPOINT = 'oss-cn-hangzhou.aliyuncs.com'
        # OSS_BUCKET_NAME = 'your-bucket-name'
        # OSS_CDN_DOMAIN = 'https://your-cdn-domain.com'
        
        self.access_key_id = getattr(config, 'OSS_ACCESS_KEY_ID', '')
        self.access_key_secret = getattr(config, 'OSS_ACCESS_KEY_SECRET', '')
        self.endpoint = getattr(config, 'OSS_ENDPOINT', '')
        self.bucket_name = getattr(config, 'OSS_BUCKET_NAME', '')
        self.cdn_domain = getattr(config, 'OSS_CDN_DOMAIN', '')
        
        self.bucket = None
        self.auth = None
        
        if self.access_key_id and self.access_key_secret:
            try:
                self.auth = oss2.Auth(self.access_key_id, self.access_key_secret)
                self.bucket = oss2.Bucket(self.auth, self.endpoint, self.bucket_name)
                print("OSS服务初始化成功")
            except Exception as e:
                print(f"OSS服务初始化失败: {e}")
    
    def upload_image(self, file_obj, prefix='images'):
        """
        上传图片到OSS
        
        Args:
            file_obj: 文件对象 (Flask的request.files中的文件)
            prefix: 文件存储前缀，例如 'avatars', 'blog', 'spots' 等
        
        Returns:
            str: 图片访问URL，失败返回None
        """
        if not self.bucket:
            print("OSS未初始化，使用本地存储")
            return None
        
        try:
            # 生成唯一文件名
            ext = os.path.splitext(file_obj.filename)[1].lower()
            if ext not in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']:
                ext = '.jpg'
            
            filename = f"{prefix}/{datetime.now().strftime('%Y%m%d')}/{uuid.uuid4().hex}{ext}"
            
            # 上传文件
            result = self.bucket.put_object(filename, file_obj)
            
            if result.status == 200:
                if self.cdn_domain:
                    return f"{self.cdn_domain}/{filename}"
                else:
                    return f"https://{self.bucket_name}.{self.endpoint}/{filename}"
            else:
                print(f"OSS上传失败: {result.status}")
                return None
                
        except Exception as e:
            print(f"OSS上传异常: {e}")
            return None
    
    def delete_image(self, file_url):
        """
        删除OSS上的图片
        
        Args:
            file_url: 完整的图片URL
        """
        if not self.bucket:
            return False
        
        try:
            # 从URL中提取文件名
            filename = file_url.split('/')[-1]
            result = self.bucket.delete_object(filename)
            return result.status == 204
        except Exception as e:
            print(f"OSS删除异常: {e}")
            return False


# 全局OSS服务实例
oss_service = OSSService()


def upload_image_to_oss(file_obj, prefix='images'):
    """
    快捷上传图片上传函数，失败时回退到本地存储
    
    Args:
        file_obj: 文件对象
        prefix: 文件存储前缀
    """
    try:
        url = oss_service.upload_image(file_obj, prefix)
        if url:
            return url
    except:
        pass
    
    # 回退到本地存储
    try:
        from utils.file_upload import save_uploaded_file
        from config import UPLOAD_FOLDER
        return save_uploaded_file(file_obj, UPLOAD_FOLDER)
    except:
        return None
