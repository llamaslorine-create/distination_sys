from flask import Blueprint, request, render_template, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from models.VisitReport import VisitReport
from models.CheckinSpot import CheckinSpot
from db import db
from sqlalchemy import func
from utils.oss_utils import oss_manager
from config import OSS_REPORT_IMAGE_DIR

bp = Blueprint('report', __name__, url_prefix='/report')

def update_spot_rating(spot_id):
    """根据探店报告更新打卡点的评分"""
    avg_rating = db.session.query(
        func.avg(VisitReport.rating)
    ).filter(
        VisitReport.spot_id == spot_id,
        VisitReport.status == 1
    ).scalar()
    
    spot = CheckinSpot.query.get(spot_id)
    if spot:
        spot.rating = float(avg_rating) if avg_rating else 0.0
        db.session.commit()

@bp.route('/list', methods=['GET'])
@login_required
def list():
    """探店报告列表 - 重定向到评论管理"""
    spot_id = request.args.get('spot_id', type=int)
    url = '/manage/comments'
    if spot_id:
        url += '?spot_id=' + str(spot_id)
    return redirect(url)

@bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    """发布探店报告"""
    spots = CheckinSpot.query.filter_by(status=1).all()
    
    if request.method == 'POST':
        spot_id = request.form['spot_id']
        title = request.form['title']
        content = request.form['content']
        rating = request.form['rating']
        
        image_url = None
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename:
                image_url, _ = oss_manager.upload_file(file, OSS_REPORT_IMAGE_DIR)
        
        try:
            report = VisitReport(
                user_id=1,
                spot_id=spot_id,
                title=title,
                content=content,
                rating=float(rating),
                image_url=image_url
            )
            db.session.add(report)
            db.session.commit()
            
            update_spot_rating(spot_id)
            
            flash('探店报告发布成功，打卡点评分已更新')
            return redirect(url_for('report.list'))
        except Exception as e:
            db.session.rollback()
            flash(f'发布失败: {str(e)}')
    
    return render_template('report/add.html', spots=spots)

@bp.route('/edit/<int:report_id>', methods=['GET', 'POST'])
@login_required
def edit(report_id):
    """编辑探店报告"""
    report = VisitReport.query.get_or_404(report_id)
    spots = CheckinSpot.query.filter_by(status=1).all()
    
    if request.method == 'POST':
        old_spot_id = report.spot_id
        new_spot_id = int(request.form['spot_id'])
        
        report.spot_id = new_spot_id
        report.title = request.form['title']
        report.content = request.form['content']
        report.rating = float(request.form['rating'])
        
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename:
                if report.image_url:
                    oss_manager.delete_file(report.image_url)
                new_url, _ = oss_manager.upload_file(file, OSS_REPORT_IMAGE_DIR)
                if new_url:
                    report.image_url = new_url
        
        try:
            db.session.commit()
            
            update_spot_rating(old_spot_id)
            if old_spot_id != new_spot_id:
                update_spot_rating(new_spot_id)
            
            flash('探店报告更新成功，打卡点评分已更新')
            return redirect(url_for('report.list'))
        except Exception as e:
            db.session.rollback()
            flash(f'更新失败: {str(e)}')
    
    return render_template('report/edit.html', report=report, spots=spots)

@bp.route('/delete/<int:report_id>')
@login_required
def delete(report_id):
    """删除探店报告"""
    report = VisitReport.query.get_or_404(report_id)
    spot_id = report.spot_id
    
    try:
        if report.image_url:
            oss_manager.delete_file(report.image_url)

        db.session.delete(report)
        db.session.commit()
        
        update_spot_rating(spot_id)
        
        flash('探店报告删除成功，打卡点评分已更新')
    except Exception as e:
        db.session.rollback()
        flash(f'删除失败: {str(e)}')
    
    return redirect(url_for('report.list'))