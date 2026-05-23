from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask_login import login_required
from models.Badge import Badge
from models.UserCheckin import UserBadge
from db import db
from utils.oss_utils import oss_manager
from config import OSS_BADGE_ICON_DIR

bp = Blueprint('badge', __name__, url_prefix='/badge')

@bp.route('/list', methods=['GET'])
@login_required
def list():
    """徽章列表"""
    page = request.args.get('page', 1, type=int)
    pagination = Badge.query.order_by(Badge.create_time.desc()).paginate(page=page, per_page=10)
    badges = pagination.items
    return render_template('badge/list.html', badges=badges, pagination=pagination)

@bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    """添加徽章"""
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        condition_type = request.form['condition_type']
        condition_value = request.form['condition_value']
        
        icon_url = None
        if 'icon' in request.files:
            file = request.files['icon']
            if file and file.filename:
                icon_url, _ = oss_manager.upload_file(file, OSS_BADGE_ICON_DIR)
        
        try:
            badge = Badge(
                name=name,
                description=description,
                icon_url=icon_url,
                condition_type=condition_type,
                condition_value=int(condition_value)
            )
            db.session.add(badge)
            db.session.commit()
            flash('徽章添加成功')
            return redirect(url_for('badge.list'))
        except Exception as e:
            db.session.rollback()
            flash(f'添加失败: {str(e)}')
    
    return render_template('badge/add.html')

@bp.route('/edit/<int:badge_id>', methods=['GET', 'POST'])
@login_required
def edit(badge_id):
    """编辑徽章"""
    badge = Badge.query.get_or_404(badge_id)
    
    if request.method == 'POST':
        badge.name = request.form['name']
        badge.description = request.form['description']
        badge.condition_type = request.form['condition_type']
        badge.condition_value = int(request.form['condition_value'])
        
        if 'icon' in request.files:
            file = request.files['icon']
            if file and file.filename:
                if badge.icon_url:
                    oss_manager.delete_file(badge.icon_url)
                new_url, _ = oss_manager.upload_file(file, OSS_BADGE_ICON_DIR)
                if new_url:
                    badge.icon_url = new_url
        
        try:
            db.session.commit()
            flash('徽章更新成功')
            return redirect(url_for('badge.list'))
        except Exception as e:
            db.session.rollback()
            flash(f'更新失败: {str(e)}')
    
    return render_template('badge/edit.html', badge=badge)

@bp.route('/delete/<int:badge_id>')
@login_required
def delete(badge_id):
    """删除徽章"""
    badge = Badge.query.get_or_404(badge_id)
    
    try:
        if badge.icon_url:
            oss_manager.delete_file(badge.icon_url)

        db.session.delete(badge)
        db.session.commit()
        flash('徽章删除成功')
    except Exception as e:
        db.session.rollback()
        flash(f'删除失败: {str(e)}')
    
    return redirect(url_for('badge.list'))

@bp.route('/user_badges', methods=['GET'])
@login_required
def user_badges():
    """用户徽章收集列表"""
    user_id = 1
    user_badges = UserBadge.query.filter_by(user_id=user_id).all()
    badges = [ub.badge for ub in user_badges]
    
    all_badges = Badge.query.all()
    obtained_count = len(badges)
    total_count = len(all_badges)
    
    return render_template('badge/user_badges.html', badges=badges, 
                          obtained_count=obtained_count, total_count=total_count)