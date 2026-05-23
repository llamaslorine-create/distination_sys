from flask import Blueprint, request, render_template, redirect, url_for, jsonify
from flask_login import login_required
from models.CheckinSpot import CheckinSpot
from models.UserCheckin import UserCheckin
from models.UserCheckin import UserBadge
from models.Badge import Badge
from db import db
from sqlalchemy import func

bp = Blueprint('map', __name__, url_prefix='/map')

@bp.route('/explore', methods=['GET'])
def explore():
    """地图探索页面"""
    return render_template('map/explore.html')

@bp.route('/checkin/<int:spot_id>', methods=['POST'])
@login_required
def checkin(spot_id):
    """打卡"""
    user_id = 1
    
    # 检查是否已打卡
    existing = UserCheckin.query.filter_by(user_id=user_id, spot_id=spot_id).first()
    if existing:
        return jsonify({'success': False, 'message': '您已经打卡过这个地点'})
    
    try:
        user_checkin = UserCheckin(user_id=user_id, spot_id=spot_id)
        db.session.add(user_checkin)
        
        # 更新打卡点计数
        spot = CheckinSpot.query.get(spot_id)
        spot.checkin_count += 1
        
        # 检查是否获得徽章
        checkin_count = UserCheckin.query.filter_by(user_id=user_id).count()
        badges = Badge.query.filter_by(
            condition_type='checkin_count',
            condition_value=checkin_count
        ).all()
        
        for badge in badges:
            existing_badge = UserBadge.query.filter_by(user_id=user_id, badge_id=badge.badge_id).first()
            if not existing_badge:
                user_badge = UserBadge(user_id=user_id, badge_id=badge.badge_id)
                db.session.add(user_badge)
        
        db.session.commit()
        return jsonify({'success': True, 'message': '打卡成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})

@bp.route('/api/user_checkins', methods=['GET'])
@login_required
def api_user_checkins():
    """获取用户已打卡的地点"""
    user_id = 1
    checkins = UserCheckin.query.filter_by(user_id=user_id).all()
    spot_ids = [c.spot_id for c in checkins]
    return jsonify({'spot_ids': spot_ids})

@bp.route('/api/spots', methods=['GET'])
@login_required
def api_spots():
    """获取所有打卡点"""
    spots = CheckinSpot.query.filter_by(status=1).all()
    data = [{
        'spot_id': s.spot_id,
        'name': s.name,
        'address': s.address,
        'latitude': s.latitude,
        'longitude': s.longitude,
        'category': s.category,
        'description': s.description,
        'rating': float(s.rating),
        'checkin_count': s.checkin_count
    } for s in spots]
    return jsonify(data)

@bp.route('/api/hotspots', methods=['GET'])
@login_required
def api_hotspots():
    """获取热门打卡点"""
    hotspots = CheckinSpot.query.filter_by(status=1).order_by(CheckinSpot.checkin_count.desc()).limit(10).all()
    data = [{
        'spot_id': h.spot_id,
        'name': h.name,
        'category': h.category,
        'checkin_count': h.checkin_count,
        'rating': float(h.rating)
    } for h in hotspots]
    return jsonify(data)

@bp.route('/api/spots/filtered', methods=['GET'])
@login_required
def api_spots_filtered():
    """获取筛选后的打卡点"""
    category = request.args.get('category')
    sort_by = request.args.get('sort', 'checkin_count')
    
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
    data = [{
        'spot_id': s.spot_id,
        'name': s.name,
        'address': s.address,
        'latitude': s.latitude,
        'longitude': s.longitude,
        'category': s.category,
        'description': s.description,
        'rating': float(s.rating),
        'checkin_count': s.checkin_count
    } for s in spots]
    return jsonify(data)

@bp.route('/api/categories', methods=['GET'])
@login_required
def api_categories():
    """获取所有分类"""
    categories = CheckinSpot.query.with_entities(CheckinSpot.category).distinct().all()
    return jsonify([c[0] for c in categories if c[0]])