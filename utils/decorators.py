"""
操作日志装饰器模块
用于自动记录管理员操作日志
"""
import functools
import logging
from flask import request
from flask_login import current_user
from models.SystemLog import SystemLog
from db import db


# 配置日志
logger = logging.getLogger(__name__)


def log_operation(operate_type):
    """操作日志装饰器

    自动记录管理员的操作日志到数据库

    Args:
        operate_type: 操作类型描述

    Returns:
        装饰器函数
    """
    def decorator(f):
        @functools.wraps(f)
        def decorated_function(*args, **kwargs):
            # 执行原始函数
            result = f(*args, **kwargs)

            # 记录操作日志（仅当用户已登录时）
            if current_user and hasattr(current_user, 'admin_id'):
                try:
                    # 获取操作内容（从请求中提取关键信息）
                    operate_content = _get_operate_content(f.__name__, kwargs)

                    # 创建日志记录
                    log = SystemLog(
                        admin_id=current_user.admin_id,
                        operate_type=operate_type,
                        operate_content=operate_content,
                        ip_address=request.remote_addr
                    )

                    # 保存日志
                    db.session.add(log)
                    db.session.commit()

                except Exception as e:
                    db.session.rollback()
                    logger.error(f"记录操作日志失败: {e}")

            return result

        return decorated_function

    return decorator


def _get_operate_content(func_name, kwargs):
    """构建操作内容描述

    Args:
        func_name: 函数名
        kwargs: 函数参数

    Returns:
        str: 操作内容描述
    """
    content_parts = []

    # 根据函数名和参数构建描述
    if 'id' in kwargs:
        content_parts.append(f"ID: {kwargs['id']}")
    if 'admin_id' in kwargs:
        content_parts.append(f"管理员ID: {kwargs['admin_id']}")
    if 'role_id' in kwargs:
        content_parts.append(f"角色ID: {kwargs['role_id']}")
    if 'novel_id' in kwargs:
        content_parts.append(f"小说ID: {kwargs['novel_id']}")
    if 'category_id' in kwargs:
        content_parts.append(f"分类ID: {kwargs['category_id']}")
    if 'user_id' in kwargs:
        content_parts.append(f"用户ID: {kwargs['user_id']}")
    if 'comment_id' in kwargs:
        content_parts.append(f"评论ID: {kwargs['comment_id']}")
    if 'carousel_id' in kwargs:
        content_parts.append(f"轮播图ID: {kwargs['carousel_id']}")

    if content_parts:
        return ', '.join(content_parts)
    else:
        return func_name


def log_admin_login(admin_id, ip_address, success=True, reason=''):
    """记录管理员登录日志

    Args:
        admin_id: 管理员ID
        ip_address: IP地址
        success: 是否登录成功
        reason: 失败原因（如果失败）
    """
    try:
        operate_type = '登录成功' if success else '登录失败'
        operate_content = f"IP: {ip_address}"
        if reason:
            operate_content += f", 原因: {reason}"

        log = SystemLog(
            admin_id=admin_id if admin_id else 0,
            operate_type=operate_type,
            operate_content=operate_content,
            ip_address=ip_address
        )

        db.session.add(log)
        db.session.commit()

    except Exception as e:
        db.session.rollback()
        logger.error(f"记录登录日志失败: {e}")