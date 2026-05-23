from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required
from models.Admin import Admin
from models.Role import Role
from models.SystemLog import SystemLog
from models.User import User
from db import db
from datetime import datetime

bp = Blueprint('system', __name__, url_prefix='/system')

@bp.route('/admin_list')
@login_required
def admin_list():
    """管理员列表"""
    admins = Admin.query.all()
    for admin in admins:
        role = Role.query.get(admin.role_id)
        admin.role_name = role.role_name if role else '-'
    return render_template('system/admin.html', admins=admins)

@bp.route('/admin/add', methods=['GET', 'POST'])
@login_required
def add_admin():
    """添加管理员"""
    if request.method == 'POST':
        account = request.form['account']
        password = request.form['password']
        name = request.form['name']
        role_id = request.form['role_id']
        
        if Admin.query.filter_by(admin_account=account).first():
            flash('账号已存在', 'error')
            return redirect(url_for('system.add_admin'))
        
        new_admin = Admin(
            admin_account=account,
            admin_password=password,
            admin_name=name,
            role_id=role_id,
            status=1,
            create_time=datetime.now(),
            update_time=datetime.now()
        )
        db.session.add(new_admin)
        db.session.commit()
        flash('管理员添加成功')
        return redirect(url_for('system.admin_list'))
    
    roles = Role.query.all()
    return render_template('system/add_admin.html', roles=roles)

@bp.route('/admin/edit/<int:admin_id>', methods=['GET', 'POST'])
@login_required
def edit_admin(admin_id):
    """编辑管理员"""
    admin = Admin.query.get(admin_id)
    if not admin:
        flash('管理员不存在', 'error')
        return redirect(url_for('system.admin_list'))
    
    if request.method == 'POST':
        admin.admin_name = request.form['name']
        admin.role_id = request.form['role_id']
        admin.status = int(request.form['status'])
        if request.form['password']:
            admin.admin_password = request.form['password']
        admin.update_time = datetime.now()
        db.session.commit()
        flash('管理员信息更新成功')
        return redirect(url_for('system.admin_list'))
    
    roles = Role.query.all()
    return render_template('system/edit_admin.html', admin=admin, roles=roles)

@bp.route('/admin/delete/<int:admin_id>', methods=['POST'])
@login_required
def delete_admin(admin_id):
    """删除管理员"""
    if admin_id == 1:
        return jsonify({'success': False, 'message': '无法删除超级管理员'})
    
    admin = Admin.query.get(admin_id)
    if not admin:
        return jsonify({'success': False, 'message': '管理员不存在'})
    
    db.session.delete(admin)
    db.session.commit()
    return jsonify({'success': True})

@bp.route('/role_list')
@login_required
def role_list():
    """角色列表"""
    roles = Role.query.all()
    return render_template('system/role.html', roles=roles)

@bp.route('/role/add', methods=['GET', 'POST'])
@login_required
def add_role():
    """添加角色"""
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        
        if Role.query.filter_by(role_name=name).first():
            flash('角色名称已存在', 'error')
            return redirect(url_for('system.add_role'))
        
        new_role = Role(
            role_name=name,
            remark=description,
            create_time=datetime.now()
        )
        db.session.add(new_role)
        db.session.commit()
        flash('角色添加成功')
        return redirect(url_for('system.role_list'))
    
    return render_template('system/add_role.html')

@bp.route('/role/edit/<int:role_id>', methods=['GET', 'POST'])
@login_required
def edit_role(role_id):
    """编辑角色"""
    role = Role.query.get(role_id)
    if not role:
        flash('角色不存在', 'error')
        return redirect(url_for('system.role_list'))
    
    if request.method == 'POST':
        role.role_name = request.form['name']
        role.remark = request.form['description']
        db.session.commit()
        flash('角色信息更新成功')
        return redirect(url_for('system.role_list'))
    
    return render_template('system/edit_role.html', role=role)

@bp.route('/role/delete/<int:role_id>', methods=['POST'])
@login_required
def delete_role(role_id):
    """删除角色"""
    role = Role.query.get(role_id)
    if not role:
        return jsonify({'success': False, 'message': '角色不存在'})
    
    if Admin.query.filter_by(role_id=role_id).first():
        return jsonify({'success': False, 'message': '该角色下还有管理员，无法删除'})
    
    db.session.delete(role)
    db.session.commit()
    return jsonify({'success': True})

@bp.route('/log_list')
@login_required
def log_list():
    """系统日志列表"""
    logs = SystemLog.query.order_by(SystemLog.operate_time.desc()).all()
    return render_template('system/log.html', logs=logs)

@bp.route('/user_list')
@login_required
def user_list():
    """用户列表"""
    users = User.query.order_by(User.create_time.desc()).all()
    return render_template('system/user_list.html', users=users)


@bp.route('/user/delete/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    """删除用户"""
    user = User.query.get(user_id)
    if not user:
        return jsonify({'success': False, 'message': '用户不存在'})
    try:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'删除失败：{str(e)}'})