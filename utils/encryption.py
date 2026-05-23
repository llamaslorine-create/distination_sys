import bcrypt


def hash_password(password):
    """密码加密
    
    Args:
        password: 原始密码字符串
    
    Returns:
        str: 加密后的密码字符串
    """
    # 生成盐并加密密码
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed.decode('utf-8')


def check_password(password, hashed_password):
    """密码验证
    
    Args:
        password: 原始密码字符串
        hashed_password: 加密后的密码字符串
    
    Returns:
        bool: 密码是否正确
    """
    # 验证密码
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))