from flask import Blueprint, render_template, jsonify
from models.CheckinSpot import CheckinSpot
from models.VisitReport import VisitReport
from models.Badge import Badge
from models.User import User
from models.CheckinRoute import CheckinRoute
from flask_login import login_required
from sqlalchemy import func, case
from db import db

bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@bp.route('/index', methods=['GET'])
@login_required
def index():
    spot_count = CheckinSpot.query.count()
    user_count = User.query.count()
    report_count = VisitReport.query.count()
    route_count = CheckinRoute.query.count()
    
    try:
        from models.BlogPost import BlogPost, BlogComment
        post_count = BlogPost.query.count()
        comment_count = BlogComment.query.count()
    except:
        post_count = 0
        comment_count = 0

    category_stats = CheckinSpot.query.with_entities(
        CheckinSpot.category, 
        func.count(CheckinSpot.spot_id)
    ).group_by(CheckinSpot.category).all()
    
    category_labels = [stat[0] for stat in category_stats] if category_stats else ['暂无数据']
    category_data = [stat[1] for stat in category_stats] if category_stats else [0]

    category_stats_with_rating = db.session.query(
        CheckinSpot.category,
        func.count(CheckinSpot.spot_id).label('count'),
        func.avg(CheckinSpot.rating).label('avg_rating'),
        func.sum(CheckinSpot.checkin_count).label('total_checkins')
    ).group_by(CheckinSpot.category).all()

    category_detail_labels = [stat[0] for stat in category_stats_with_rating] if category_stats_with_rating else ['暂无数据']
    category_detail_counts = [stat[1] for stat in category_stats_with_rating] if category_stats_with_rating else [0]
    category_avg_ratings = [round(float(stat[2]), 1) if stat[2] else 0 for stat in category_stats_with_rating] if category_stats_with_rating else [0]
    category_total_checkins = [stat[3] for stat in category_stats_with_rating] if category_stats_with_rating else [0]

    top_spots = CheckinSpot.query.filter(CheckinSpot.checkin_count > 0).order_by(CheckinSpot.checkin_count.desc()).limit(10).all()
    spot_names = [s.name for s in top_spots]
    spot_counts = [s.checkin_count or 0 for s in top_spots]
    spot_ratings = [float(s.rating) if s.rating else 0 for s in top_spots]
    
    top_rated_spots = CheckinSpot.query.filter(
        CheckinSpot.rating.isnot(None),
        CheckinSpot.rating > 0
    ).order_by(CheckinSpot.rating.desc()).limit(10).all()
    rated_spot_names = [s.name for s in top_rated_spots]
    rated_spot_scores = [float(s.rating) if s.rating else 0 for s in top_rated_spots]
    rated_spot_checkins = [s.checkin_count or 0 for s in top_rated_spots]

    top_comprehensive_spots = CheckinSpot.query.filter(
        CheckinSpot.rating.isnot(None),
        CheckinSpot.rating > 0,
        CheckinSpot.checkin_count > 0
    ).order_by(
        (CheckinSpot.rating * 0.6 + case(
            (CheckinSpot.checkin_count / 100 > 5, 5),
            else_=CheckinSpot.checkin_count / 100
        ) * 0.4).desc()
    ).limit(10).all()
    comprehensive_spot_names = [s.name for s in top_comprehensive_spots]
    comprehensive_spot_scores = [float(s.rating) if s.rating else 0 for s in top_comprehensive_spots]
    comprehensive_spot_checkins = [s.checkin_count or 0 for s in top_comprehensive_spots]

    return render_template(
        'dashboard.html',
        spot_count=spot_count,
        user_count=user_count,
        report_count=report_count,
        route_count=route_count,
        post_count=post_count,
        comment_count=comment_count,
        category_labels=category_labels,
        category_data=category_data,
        category_detail_labels=category_detail_labels,
        category_detail_counts=category_detail_counts,
        category_avg_ratings=category_avg_ratings,
        category_total_checkins=category_total_checkins,
        spot_names=spot_names,
        spot_counts=spot_counts,
        spot_ratings=spot_ratings,
        rated_spot_names=rated_spot_names,
        rated_spot_scores=rated_spot_scores,
        rated_spot_checkins=rated_spot_checkins,
        comprehensive_spot_names=comprehensive_spot_names,
        comprehensive_spot_scores=comprehensive_spot_scores,
        comprehensive_spot_checkins=comprehensive_spot_checkins
    )

@bp.route('/api/stats', methods=['GET'])
@login_required
def get_stats():
    try:
        from models.BlogPost import BlogPost, BlogComment
        post_count = BlogPost.query.count()
        comment_count = BlogComment.query.count()
    except:
        post_count = 0
        comment_count = 0
        
    return jsonify({
        'spots': CheckinSpot.query.count(),
        'users': User.query.count(),
        'reports': VisitReport.query.count(),
        'routes': CheckinRoute.query.count(),
        'posts': post_count,
        'comments': comment_count
    })