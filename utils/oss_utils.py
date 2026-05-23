import os
import uuid
from flask import current_app
from datetime import datetime

try:
    from oss2 import Auth, Bucket, exceptions
    OSS_AVAILABLE = True
except ImportError:
    OSS_AVAILABLE = False

class OSSManager:
    def __init__(self):
        self.auth = None
        self.bucket = None
    
    def _init_bucket(self):
        if not OSS_AVAILABLE:
            print("[OSS-TRACE] _init_bucket: oss2 not importable, skip", flush=True)
            return

        try:
            access_key_id = current_app.config.get('OSS_ACCESS_KEY_ID')
            access_key_secret = current_app.config.get('OSS_ACCESS_KEY_SECRET')
            endpoint = current_app.config.get('OSS_ENDPOINT')
            bucket_name = current_app.config.get('OSS_BUCKET_NAME')

            print(f"[OSS-TRACE] _init_bucket: ak_id={'*' * 4 + (access_key_id or '')[-4:] if access_key_id else None} ak_secret_set={bool(access_key_secret)} endpoint={endpoint} bucket={bucket_name}", flush=True)

            if access_key_id and access_key_secret and endpoint and bucket_name:
                self.auth = Auth(access_key_id, access_key_secret)
                self.bucket = Bucket(self.auth, endpoint, bucket_name)
                print(f"[OSS-TRACE] _init_bucket: bucket constructed OK", flush=True)
            else:
                print(f"[OSS-TRACE] _init_bucket: 配置缺失，未构造 bucket", flush=True)
        except Exception as e:
            print(f"[OSS-TRACE] _init_bucket: 异常 [{type(e).__name__}]: {e}", flush=True)
            import traceback
            traceback.print_exc()
    
    def _generate_filename(self, original_filename, directory=''):
        ext = os.path.splitext(original_filename)[1].lower()
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        unique_id = str(uuid.uuid4())[:8]
        return f"{directory}{timestamp}_{unique_id}{ext}"
    
    def upload_file(self, file, directory=''):
        if not file or file.filename == '':
            return None, "文件为空"

        use_oss = current_app.config.get('USE_OSS', False)
        print(f"[OSS-TRACE] upload_file called: filename={file.filename!r} dir={directory!r} USE_OSS={use_oss}", flush=True)

        # 每次上传都重新初始化，解决Flask调试模式重新加载问题
        if use_oss:
            self._init_bucket()

        if not self.bucket or not use_oss:
            print(f"[OSS-TRACE] -> 走本地（bucket={self.bucket!r}, use_oss={use_oss}）", flush=True)
            return self._upload_local(file, directory)

        try:
            filename = self._generate_filename(file.filename, directory)
            file.seek(0)
            content = file.read()
            print(f"[OSS-TRACE] -> 准备 PutObject: key={filename}, size={len(content)}", flush=True)
            result = self.bucket.put_object(filename, content, headers={'x-oss-object-acl': 'public-read'})

            if result.status == 200:
                url_prefix = current_app.config.get('OSS_URL_PREFIX', '')
                full_url = f"{url_prefix}/{filename}"
                print(f"[OSS-TRACE] -> OK: {full_url}", flush=True)
                return full_url, None
            else:
                print(f"[OSS-TRACE] -> 异常状态码 {result.status}, 回退本地", flush=True)
                file.seek(0)
                return self._upload_local(file, directory)
        except exceptions.OssError as e:
            print(f"[OSS-TRACE] -> OssError: code={getattr(e,'code','?')} status={getattr(e,'status','?')} msg={getattr(e,'message','?')[:200]} req_id={getattr(e,'request_id','?')} -> 回退本地", flush=True)
            file.seek(0)
            return self._upload_local(file, directory)
        except Exception as e:
            print(f"[OSS-TRACE] -> 未知异常 [{type(e).__name__}]: {e} -> 回退本地", flush=True)
            file.seek(0)
            return self._upload_local(file, directory)
    
    def _upload_local(self, file, directory=''):
        try:
            filename = self._generate_filename(file.filename, '')
            upload_folder = current_app.config.get('UPLOAD_FOLDER', 'static/uploads')
            
            if directory:
                folder = os.path.join(upload_folder, directory.rstrip('/'))
            else:
                folder = upload_folder
            
            if not os.path.exists(folder):
                os.makedirs(folder)
            
            file_path = os.path.join(folder, filename)
            file.seek(0)
            file.save(file_path)
            
            return f"/static/uploads/{directory}{filename}", None
        except Exception as e:
            current_app.logger.error(f"本地上传失败: {e}")
            return None, str(e)
    
    def delete_file(self, file_url):
        if not file_url:
            return True
        
        use_oss = current_app.config.get('USE_OSS', False)
        if use_oss and not self.bucket:
            self._init_bucket()
        
        if not self.bucket or not use_oss:
            return self._delete_local(file_url)
        
        try:
            if 'http://' in file_url or 'https://' in file_url:
                key = file_url.replace(current_app.config.get('OSS_URL_PREFIX', '') + '/', '')
            else:
                key = file_url.lstrip('/')
            
            self.bucket.delete_object(key)
            return True
        except exceptions.OssError as e:
            current_app.logger.error(f"OSS删除失败: {e}")
            return False
        except Exception as e:
            current_app.logger.error(f"删除失败: {e}")
            return False
    
    def _delete_local(self, file_url):
        try:
            if 'http://' in file_url or 'https://' in file_url:
                return True
            
            file_path = os.path.join(current_app.root_path, file_url.lstrip('/'))
            if os.path.exists(file_path):
                os.remove(file_path)
            return True
        except Exception as e:
            current_app.logger.error(f"本地删除失败: {e}")
            return False
    
    def get_file_url(self, filename, directory=''):
        if self.bucket and current_app.config.get('USE_OSS', False):
            return f"{current_app.config.get('OSS_URL_PREFIX', '')}/{directory}{filename}"
        else:
            return f"/static/uploads/{directory}{filename}"

oss_manager = OSSManager()

def init_oss(app):
    global oss_manager
    with app.app_context():
        oss_manager = OSSManager()
        oss_manager._init_bucket()