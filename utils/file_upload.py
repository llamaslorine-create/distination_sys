import os
import uuid
from werkzeug.utils import secure_filename
from config import ALLOWED_EXTENSIONS, UPLOAD_FOLDER, MAX_CONTENT_LENGTH


def allowed_file(filename, allowed_extensions=None):
    """检查文件扩展名是否允许

    Args:
        filename: 文件名
        allowed_extensions: 允许的扩展名集合，默认为配置中的图片扩展名

    Returns:
        bool: 是否允许上传
    """
    if allowed_extensions is None:
        allowed_extensions = ALLOWED_EXTENSIONS
    
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions


def generate_unique_filename(filename):
    """生成唯一的文件名，避免文件名冲突

    Args:
        filename: 原始文件名

    Returns:
        str: 唯一的文件名
    """
    # 获取文件扩展名
    ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
    # 生成UUID作为文件名
    unique_name = f"{uuid.uuid4().hex}"
    # 返回带扩展名的文件名
    return f"{unique_name}.{ext}" if ext else unique_name


def save_uploaded_file(file, upload_folder=None):
    """安全地保存上传的文件

    Args:
        file: Flask文件对象
        upload_folder: 上传目录，默认为配置中的上传目录

    Returns:
        str: 保存后的文件名，如果失败返回None
    """
    if upload_folder is None:
        upload_folder = UPLOAD_FOLDER
    
    # 确保上传目录存在
    os.makedirs(upload_folder, exist_ok=True)
    
    if file and allowed_file(file.filename):
        # 安全处理文件名
        secure_name = secure_filename(file.filename)
        # 生成唯一文件名
        unique_name = generate_unique_filename(secure_name)
        # 保存文件
        file_path = os.path.join(upload_folder, unique_name)
        file.save(file_path)
        return unique_name
    
    return None


def get_file_size(file):
    """获取文件大小（字节）

    Args:
        file: Flask文件对象

    Returns:
        int: 文件大小
    """
    file.seek(0, os.SEEK_END)
    size = file.tell()
    file.seek(0)
    return size


def is_file_size_allowed(file, max_size=None):
    """检查文件大小是否在允许范围内

    Args:
        file: Flask文件对象
        max_size: 最大文件大小（字节），默认为配置中的最大值

    Returns:
        bool: 是否允许
    """
    if max_size is None:
        max_size = MAX_CONTENT_LENGTH
    
    return get_file_size(file) <= max_size