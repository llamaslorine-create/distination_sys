from flask import Blueprint, request, render_template, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from models.CheckinSpot import CheckinSpot
from models.VisitReport import VisitReport
from models.UserCheckin import UserCheckin
from db import db
from sqlalchemy import func
import re
from utils.oss_utils import oss_manager
from config import OSS_SPOT_IMAGE_DIR

bp = Blueprint('checkin', __name__, url_prefix='/checkin')

def dms_to_decimal(dms_str):
    """将度分秒格式转换为十进制"""
    dms_str = dms_str.strip()
    
    dms_str = dms_str.strip('"\'')
    
    if dms_str.replace('.', '').replace('-', '').replace(' ', '').isdigit():
        return float(dms_str)
    
    pattern = r'(-?\d+)[°度]\s*(\d+)[\'分]\s*([\d.]+)[\"秒]?'
    match = re.match(pattern, dms_str)
    
    if match:
        degrees = int(match.group(1))
        minutes = int(match.group(2))
        seconds = float(match.group(3))
        
        decimal = abs(degrees) + minutes / 60 + seconds / 3600
        if degrees < 0:
            decimal = -decimal
        return decimal
    
    try:
        return float(dms_str)
    except ValueError:
        raise ValueError(f"无法解析坐标格式: {dms_str}")

@bp.route('/list', methods=['GET'])
@login_required
def list():
    """打卡点列表"""
    page = request.args.get('page', 1, type=int)
    keyword = request.args.get('keyword', '')
    category = request.args.get('category', '')
    
    query = CheckinSpot.query
    
    if keyword:
        query = query.filter(CheckinSpot.name.like(f'%{keyword}%'))
    if category:
        query = query.filter(CheckinSpot.category == category)
    
    pagination = query.order_by(CheckinSpot.spot_id.asc()).paginate(page=page, per_page=10)
    spots = pagination.items
    
    categories = CheckinSpot.query.with_entities(CheckinSpot.category).distinct().all()
    category_list = [cat[0] for cat in categories]
    
    return render_template('checkin/list.html', spots=spots, pagination=pagination, 
                           keyword=keyword, category=category, category_list=category_list)

@bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    """添加打卡点"""
    if request.method == 'POST':
        name = request.form['name']
        address = request.form['address']
        latitude = request.form['latitude']
        longitude = request.form['longitude']
        category = request.form['category']
        description = request.form['description']
        
        image_url = None
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename:
                image_url, _ = oss_manager.upload_file(file, OSS_SPOT_IMAGE_DIR)
        
        try:
            lat = dms_to_decimal(latitude)
            lng = dms_to_decimal(longitude)
            
            spot = CheckinSpot(
                name=name,
                address=address,
                latitude=lat,
                longitude=lng,
                category=category,
                description=description,
                image_url=image_url
            )
            db.session.add(spot)
            db.session.commit()
            flash('打卡点添加成功，已跳转到地图页面')
            return redirect(url_for('map.explore'))
        except Exception as e:
            db.session.rollback()
            flash(f'添加失败: {str(e)}')
    
    return render_template('checkin/add.html')

@bp.route('/edit/<int:spot_id>', methods=['GET', 'POST'])
@login_required
def edit(spot_id):
    """编辑打卡点"""
    spot = CheckinSpot.query.get_or_404(spot_id)
    
    if request.method == 'POST':
        spot.name = request.form['name']
        spot.address = request.form['address']
        spot.latitude = dms_to_decimal(request.form['latitude'])
        spot.longitude = dms_to_decimal(request.form['longitude'])
        spot.category = request.form['category']
        spot.description = request.form['description']
        
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename:
                if spot.image_url:
                    oss_manager.delete_file(spot.image_url)
                new_url, _ = oss_manager.upload_file(file, OSS_SPOT_IMAGE_DIR)
                if new_url:
                    spot.image_url = new_url
        
        try:
            db.session.commit()
            flash('打卡点更新成功')
            return redirect(url_for('checkin.list'))
        except Exception as e:
            db.session.rollback()
            flash(f'更新失败: {str(e)}')
    
    return render_template('checkin/edit.html', spot=spot)

@bp.route('/delete/<int:spot_id>')
@login_required
def delete(spot_id):
    """删除打卡点"""
    spot = CheckinSpot.query.get_or_404(spot_id)
    
    try:
        # 删除图片
        if spot.image_url:
            oss_manager.delete_file(spot.image_url)

        db.session.delete(spot)
        db.session.commit()
        flash('打卡点删除成功')
    except Exception as e:
        db.session.rollback()
        flash(f'删除失败: {str(e)}')
    
    return redirect(url_for('checkin.list'))

@bp.route('/stats', methods=['GET'])
@login_required
def stats():
    """打卡点统计分析"""
    # 按分类统计打卡点数量
    category_stats = CheckinSpot.query.with_entities(
        CheckinSpot.category,
        func.count(CheckinSpot.spot_id)
    ).group_by(CheckinSpot.category).all()
    
    # 按区域热度统计（模拟区域划分）
    area_stats = CheckinSpot.query.with_entities(
        func.substr(CheckinSpot.address, 1, 3).label('area'),
        func.count(CheckinSpot.spot_id)
    ).group_by('area').order_by(func.count(CheckinSpot.spot_id).desc()).limit(10).all()
    
    # 新点探索趋势（按月份）
    monthly_stats = db.session.query(
        func.date_format(CheckinSpot.create_time, '%Y-%m').label('month'),
        func.count(CheckinSpot.spot_id)
    ).group_by('month').order_by('month').limit(12).all()
    
    categories = [stat[0] for stat in category_stats]
    category_counts = [stat[1] for stat in category_stats]
    
    areas = [stat[0] for stat in area_stats]
    area_counts = [stat[1] for stat in area_stats]
    
    months = [stat[0] for stat in monthly_stats]
    monthly_counts = [stat[1] for stat in monthly_stats]
    
    return render_template('checkin/stats.html',
                          categories=categories, category_counts=category_counts,
                          areas=areas, area_counts=area_counts,
                          months=months, monthly_counts=monthly_counts)

@bp.route('/', methods=['GET'])
@login_required
def index():
    """用户端打卡评分首页"""
    category = request.args.get('category')
    sort_by = request.args.get('sort_by', 'checkin_count')
    
    query = CheckinSpot.query.filter_by(status=1)
    
    if category:
        query = query.filter_by(category=category)
    
    if sort_by == 'checkin_count':
        query = query.order_by(CheckinSpot.checkin_count.desc())
    elif sort_by == 'rating':
        query = query.order_by(CheckinSpot.rating.desc())
    elif sort_by == 'name':
        query = query.order_by(CheckinSpot.name)
    
    spots = query.all()
    
    for spot in spots:
        reports = VisitReport.query.filter_by(spot_id=spot.spot_id, status=1).order_by(VisitReport.create_time.desc()).all()
        spot.reports = reports
        spot.report_count = len(reports)
    
    categories = CheckinSpot.query.with_entities(CheckinSpot.category).distinct().all()
    category_list = [cat[0] for cat in categories if cat[0]]
    
    checked_spots = set()
    if hasattr(current_user, 'user_id') and current_user.user_id:
        user_checkins = UserCheckin.query.filter_by(user_id=current_user.user_id).all()
        checked_spots = {c.spot_id for c in user_checkins}
    
    return render_template('checkin/user_index.html', 
                           spots=spots, 
                           categories=category_list,
                           selected_category=category,
                           sort_by=sort_by,
                           checked_spots=checked_spots)

@bp.route('/do_checkin/<int:spot_id>', methods=['POST'])
@login_required
def do_checkin(spot_id):
    """用户打卡"""
    if not hasattr(current_user, 'user_id') or not current_user.user_id:
        return jsonify({'success': False, 'message': '只有普通用户才能打卡'})

    try:
        spot = CheckinSpot.query.get_or_404(spot_id)

        existed = UserCheckin.query.filter_by(user_id=current_user.user_id, spot_id=spot_id).first()
        if existed:
            return jsonify({'success': False, 'message': '您已打卡过这个地点啦', 'checkin_count': spot.checkin_count})

        user_checkin = UserCheckin(
            user_id=current_user.user_id,
            spot_id=spot_id
        )
        db.session.add(user_checkin)

        spot.checkin_count += 1
        db.session.commit()

        return jsonify({'success': True, 'message': '打卡成功！', 'checkin_count': spot.checkin_count})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})

@bp.route('/rate/<int:spot_id>', methods=['POST'])
@login_required
def rate(spot_id):
    """用户评分：不写回 spot.rating，只返回当前 spot 的总评分用于前端反馈"""
    try:
        score = float(request.form.get('score'))
        if score < 1 or score > 5:
            return jsonify({'success': False, 'message': '评分必须在1-5之间'})

        spot = CheckinSpot.query.get_or_404(spot_id)
        return jsonify({'success': True, 'message': '感谢您的评分！', 'rating': spot.rating})
    except ValueError:
        return jsonify({'success': False, 'message': '请输入有效的评分'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})

@bp.route('/add_comment/<int:spot_id>', methods=['POST'])
@login_required
def add_comment(spot_id):
    """用户评论打卡点"""
    if not hasattr(current_user, 'user_id') or not current_user.user_id:
        return jsonify({'success': False, 'message': '只有普通用户才能评论'})
    
    try:
        content = request.form.get('content')
        if not content or not content.strip():
            return jsonify({'success': False, 'message': '请输入评论内容'})
        
        report = VisitReport(
            spot_id=spot_id,
            user_id=current_user.user_id,
            title='',
            content=content,
            rating=0,
            status=1
        )
        
        db.session.add(report)
        db.session.commit()
        
        return jsonify({'success': True, 'message': '评论成功！'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})

@bp.route('/api/spots', methods=['GET'])
def api_spots():
    """获取打卡点数据API"""
    spots = CheckinSpot.query.filter_by(status=1).all()
    data = [{
        'spot_id': s.spot_id,
        'name': s.name,
        'address': s.address,
        'latitude': s.latitude,
        'longitude': s.longitude,
        'category': s.category,
        'rating': float(s.rating),
        'checkin_count': s.checkin_count
    } for s in spots]
    return jsonify(data)