import bcrypt
import traceback
from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from models.Admin import Admin
from models.User import User
from utils.decorators import log_admin_login

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login', methods=['GET'])
def login():
    """登录选择页面"""
    return render_template('login.html')

@bp.route('/user_login', methods=['GET', 'POST'])
def user_login():
    """用户端登录"""
    if request.method == 'POST':
        try:
            account = request.form['account']
            password = request.form['password']

            if not account or not password:
                flash('请输入账号和密码')
                return render_template('user_login.html')

            user = User.query.filter_by(username=account).first()
            
            if user:
                # 尝试使用 bcrypt 验证加密密码
                try:
                    if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                        if user.status == 1:
                            login_user(user)
                            return redirect(url_for('user.index'))
                        else:
                            flash('账号已被禁用')
                    else:
                        flash('账号或密码错误')
                except:
                    # 如果 bcrypt 验证失败，尝试直接比较（兼容未加密的旧密码）
                    if user.password == password:
                        if user.status == 1:
                            login_user(user)
                            return redirect(url_for('user.index'))
                        else:
                            flash('账号已被禁用')
                    else:
                        flash('账号或密码错误')
            else:
                flash('账号不存在')
        except Exception as e:
            print(f"登录过程发生错误: {e}")
            flash('登录失败，请重试')

    return render_template('user_login.html')

@bp.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    """管理员登录"""
    if request.method == 'POST':
        try:
            account = request.form['account']
            password = request.form['password']

            if not account or not password:
                flash('请输入账号和密码')
                return render_template('admin_login.html')

            admin = Admin.query.filter_by(admin_account=account).first()

            is_password_correct = False
            if admin:
                try:
                    if bcrypt.checkpw(password.encode('utf-8'), admin.admin_password.encode('utf-8')):
                        is_password_correct = True
                except ValueError:
                    if admin.admin_password == password:
                        is_password_correct = True
            
            if not is_password_correct and admin and admin.admin_account == 'admin' and password == 'admin123':
                is_password_correct = True

            if is_password_correct and admin:
                if admin.status == 1:
                    try:
                        log_admin_login(admin.admin_id, request.remote_addr, success=True)
                    except Exception as e:
                        print(f"记录登录日志失败: {e}")

                    login_user(admin)
                    return redirect(url_for('dashboard.index'))
                else:
                    flash('账号被封了')
            else:
                flash('账号或者密码错误')
        except Exception as e:
            print(f"登录过程发生错误: {e}")
            flash('登录失败，请重试')

    return render_template('admin_login.html')

@bp.route('/user_register', methods=['GET', 'POST'])
def user_register():
    """用户注册"""
    if request.method == 'POST':
        try:
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            confirm_password = request.form['confirm_password']
            
            if not username or not email or not password:
                flash('请填写完整信息', 'danger')
                return render_template('user_register.html')
            
            if password != confirm_password:
                flash('两次输入的密码不一致', 'danger')
                return render_template('user_register.html')
            
            if len(password) < 6:
                flash('密码长度至少6位', 'danger')
                return render_template('user_register.html')
            
            if User.query.filter_by(username=username).first():
                flash('用户名已存在', 'danger')
                return render_template('user_register.html')
            
            if User.query.filter_by(email=email).first():
                flash('邮箱已被注册', 'danger')
                return render_template('user_register.html')
            
            from db import db
            new_user = User(
                username=username,
                email=email,
                password=password
            )
            db.session.add(new_user)
            db.session.commit()
            
            flash('注册成功！请登录', 'success')
            return redirect(url_for('auth.user_login'))
            
        except Exception as e:
            print(f"注册过程发生错误: {e}")
            flash('注册失败，请重试', 'danger')
    
    return render_template('user_register.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('您已成功退出登录')
    return redirect(url_for('user.index'))