from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask_login import login_required
from models.CheckinRoute import CheckinRoute, RouteSpot
from models.CheckinSpot import CheckinSpot
from db import db
from utils.oss_utils import oss_manager
from config import OSS_ROUTE_COVER_DIR

bp = Blueprint('route', __name__, url_prefix='/route')

@bp.route('/list', methods=['GET'])
@login_required
def list():
    """打卡路线列表（管理员）"""
    page = request.args.get('page', 1, type=int)
    
    pagination = CheckinRoute.query.order_by(CheckinRoute.create_time.desc()).paginate(page=page, per_page=10)
    
    routes = pagination.items
    
    for route in routes:
        spots = RouteSpot.query.filter_by(route_id=route.route_id).all()
        route.spots = spots
    
    return render_template('route/list.html', routes=routes, pagination=pagination)

@bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    """创建打卡路线"""
    spots = CheckinSpot.query.filter_by(status=1).all()
    
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        spot_ids = request.form.getlist('spot_ids')
        
        cover_image = None
        if 'cover' in request.files:
            file = request.files['cover']
            if file and file.filename:
                cover_image, _ = oss_manager.upload_file(file, OSS_ROUTE_COVER_DIR)
        
        try:
            route = CheckinRoute(
                user_id=1,
                name=name,
                description=description,
                cover_image=cover_image
            )
            db.session.add(route)
            db.session.commit()
            
            for i, spot_id in enumerate(spot_ids):
                route_spot = RouteSpot(
                    route_id=route.route_id,
                    spot_id=int(spot_id),
                    order_num=i + 1
                )
                db.session.add(route_spot)
            
            db.session.commit()
            flash('打卡路线创建成功')
            return redirect(url_for('route.list'))
        except Exception as e:
            db.session.rollback()
            flash(f'创建失败: {str(e)}')
    
    return render_template('route/add.html', spots=spots)

@bp.route('/edit/<int:route_id>', methods=['GET', 'POST'])
@login_required
def edit(route_id):
    """编辑打卡路线"""
    route = CheckinRoute.query.get_or_404(route_id)
    spots = CheckinSpot.query.filter_by(status=1).all()
    
    if request.method == 'POST':
        route.name = request.form['name']
        route.description = request.form['description']
        spot_ids = request.form.getlist('spot_ids')
        
        if 'cover' in request.files:
            file = request.files['cover']
            if file and file.filename:
                if route.cover_image:
                    oss_manager.delete_file(route.cover_image)
                new_url, _ = oss_manager.upload_file(file, OSS_ROUTE_COVER_DIR)
                if new_url:
                    route.cover_image = new_url
        
        try:
            # 删除旧的路线点关联
            RouteSpot.query.filter_by(route_id=route_id).delete()
            
            for i, spot_id in enumerate(spot_ids):
                route_spot = RouteSpot(
                    route_id=route.route_id,
                    spot_id=int(spot_id),
                    order_num=i + 1
                )
                db.session.add(route_spot)
            
            db.session.commit()
            flash('打卡路线更新成功')
            return redirect(url_for('route.list'))
        except Exception as e:
            db.session.rollback()
            flash(f'更新失败: {str(e)}')
    
    route_spot_ids = [rs.spot_id for rs in RouteSpot.query.filter_by(route_id=route.route_id).order_by(RouteSpot.order_num).all()]
    
    return render_template('route/edit.html', route=route, spots=spots, 
                          route_spot_ids=route_spot_ids)

@bp.route('/delete/<int:route_id>')
@login_required
def delete(route_id):
    """删除打卡路线"""
    route = CheckinRoute.query.get_or_404(route_id)
    
    try:
        if route.cover_image:
            oss_manager.delete_file(route.cover_image)

        db.session.delete(route)
        db.session.commit()
        flash('打卡路线删除成功')
    except Exception as e:
        db.session.rollback()
        flash(f'删除失败: {str(e)}')
    
    return redirect(url_for('route.list'))

@bp.route('/view/<int:route_id>', methods=['GET'])
@login_required
def view(route_id):
    """查看路线详情（管理员）"""
    route = CheckinRoute.query.get_or_404(route_id)
    route_spots = RouteSpot.query.filter_by(route_id=route.route_id).order_by(RouteSpot.order_num).all()
    spots = [rs.spot for rs in route_spots]
    
    return render_template('route/detail.html', route=route, spots=spots)

@bp.route('/map/<int:route_id>', methods=['GET'])
@login_required
def map_view(route_id):
    """在地图上查看路线"""
    route = CheckinRoute.query.get_or_404(route_id)
    route_spots = RouteSpot.query.filter_by(route_id=route.route_id).order_by(RouteSpot.order_num).all()
    spots = [rs.spot for rs in route_spots]
    
    # 准备地图标记数据
    markers = []
    for i, spot in enumerate(spots):
        markers.append({
            'id': spot.spot_id,
            'name': spot.name,
            'address': spot.address,
            'latitude': float(spot.latitude),
            'longitude': float(spot.longitude),
            'order': i + 1,
            'image_url': spot.image_url
        })
    
    # 计算中心点
    if markers:
        avg_lat = sum(m['latitude'] for m in markers) / len(markers)
        avg_lng = sum(m['longitude'] for m in markers) / len(markers)
    else:
        avg_lat, avg_lng = 30.5928, 114.3055
    
    return render_template('route/map_view.html', route=route, spots=spots, markers=markers, 
                          center_lat=avg_lat, center_lng=avg_lng)