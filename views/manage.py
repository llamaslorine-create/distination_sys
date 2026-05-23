from flask import Blueprint, render_template, request, flash, redirect, url_for
from models.Announcement import Announcement
from models.BlogPost import BlogPost, BlogComment
from models.VisitReport import VisitReport
from models.CheckinSpot import CheckinSpot
from models.User import User
from db import db
from flask_login import login_required, current_user

bp = Blueprint('manage', __name__, url_prefix='/manage')

@bp.route('/announcements', methods=['GET'])
@login_required
def announcements():
    page = request.args.get('page', 1, type=int)
    pagination = Announcement.query.order_by(Announcement.create_time.desc()).paginate(page=page, per_page=10)
    return render_template('manage/announcements.html', pagination=pagination, items=pagination.items)

@bp.route('/announcement/add', methods=['GET', 'POST'])
@login_required
def add_announcement():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        image_url = request.form.get('image_url', '')
        
        try:
            announcement = Announcement(
                title=title,
                content=content,
                image_url=image_url,
                admin_id=current_user.id if hasattr(current_user, 'id') else 1
            )
            db.session.add(announcement)
            db.session.commit()
            flash('公告添加成功！')
            return redirect(url_for('manage.announcements'))
        except Exception as e:
            db.session.rollback()
            flash(f'添加失败：{str(e)}', 'error')
    
    return render_template('manage/announcement_form.html')

@bp.route('/announcement/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_announcement(id):
    announcement = Announcement.query.get_or_404(id)
    
    if request.method == 'POST':
        announcement.title = request.form['title']
        announcement.content = request.form['content']
        announcement.image_url = request.form.get('image_url', '')
        
        try:
            db.session.commit()
            flash('公告更新成功！')
            return redirect(url_for('manage.announcements'))
        except Exception as e:
            db.session.rollback()
            flash(f'更新失败：{str(e)}', 'error')
    
    return render_template('manage/announcement_form.html', item=announcement)

@bp.route('/announcement/delete/<int:id>', methods=['GET'])
@login_required
def delete_announcement(id):
    announcement = Announcement.query.get_or_404(id)
    try:
        db.session.delete(announcement)
        db.session.commit()
        flash('公告删除成功！')
    except Exception as e:
        db.session.rollback()
        flash(f'删除失败：{str(e)}', 'error')
    
    return redirect(url_for('manage.announcements'))

@bp.route('/posts', methods=['GET'])
@login_required
def posts():
    page = request.args.get('page', 1, type=int)
    pagination = BlogPost.query.order_by(BlogPost.create_time.desc()).paginate(page=page, per_page=10)
    return render_template('manage/posts.html', pagination=pagination, items=pagination.items)

@bp.route('/post/status/<int:id>', methods=['GET'])
@login_required
def toggle_post_status(id):
    post = BlogPost.query.get_or_404(id)
    post.status = 0 if post.status == 1 else 1
    db.session.commit()
    flash('帖子状态已更新！')
    return redirect(url_for('manage.posts'))

@bp.route('/post/delete/<int:id>', methods=['GET'])
@login_required
def delete_post(id):
    post = BlogPost.query.get_or_404(id)
    try:
        db.session.delete(post)
        db.session.commit()
        flash('帖子删除成功！')
    except Exception as e:
        db.session.rollback()
        flash(f'删除失败：{str(e)}', 'error')
    
    return redirect(url_for('manage.posts'))

@bp.route('/post/comments/<int:id>', methods=['GET'])
@login_required
def post_comments(id):
    post = BlogPost.query.get_or_404(id)
    comments = BlogComment.query.filter_by(post_id=id).order_by(BlogComment.create_time.desc()).all()
    return render_template('manage/post_comments.html', post=post, comments=comments)

@bp.route('/post/comment/status/<int:id>', methods=['GET'])
@login_required
def toggle_post_comment_status(id):
    comment = BlogComment.query.get_or_404(id)
    comment.status = 0 if comment.status == 1 else 1
    db.session.commit()
    flash('评论状态已更新！')
    referer = request.headers.get('Referer', '')
    if 'post_comments' in referer:
        return redirect(request.referrer)
    return redirect(url_for('manage.post_comments', id=comment.post_id))

@bp.route('/post/comment/delete/<int:id>', methods=['GET'])
@login_required
def delete_post_comment(id):
    comment = BlogComment.query.get_or_404(id)
    post_id = comment.post_id
    try:
        db.session.delete(comment)
        db.session.commit()
        flash('评论删除成功！')
    except Exception as e:
        db.session.rollback()
        flash(f'删除失败：{str(e)}', 'error')
    return redirect(url_for('manage.post_comments', id=post_id))

@bp.route('/comments', methods=['GET'])
@login_required
def comments():
    spot_id = request.args.get('spot_id', type=int)
    status_filter = request.args.get('status', type=int, default=1)
    source = request.args.get('source', default='all')  # all / spot / blog

    spots = CheckinSpot.query.filter_by(status=1).all()

    spot_comments = {}
    if source in ('all', 'spot'):
        query = VisitReport.query
        if status_filter != 2:
            query = query.filter_by(status=status_filter)
        if spot_id:
            query = query.filter_by(spot_id=spot_id)

        reports = query.order_by(VisitReport.create_time.desc()).all()
        for report in reports:
            spot = CheckinSpot.query.get(report.spot_id)
            user = User.query.get(report.user_id)
            if spot:
                if spot.spot_id not in spot_comments:
                    spot_comments[spot.spot_id] = {'spot': spot, 'comments': []}
                spot_comments[spot.spot_id]['comments'].append({
                    'report': report, 'user': user
                })

    blog_groups = {}
    if source in ('all', 'blog'):
        bquery = BlogComment.query
        if status_filter != 2:
            bquery = bquery.filter_by(status=status_filter)
        bcomments = bquery.order_by(BlogComment.create_time.desc()).all()
        for c in bcomments:
            post = BlogPost.query.get(c.post_id)
            if not post:
                continue
            if post.post_id not in blog_groups:
                blog_groups[post.post_id] = {'post': post, 'comments': []}
            blog_groups[post.post_id]['comments'].append(c)

    return render_template('manage/comments.html',
                           spots=spots,
                           spot_comments=spot_comments,
                           blog_groups=blog_groups,
                           selected_spot=spot_id,
                           status_filter=status_filter,
                           source=source)

@bp.route('/comment/status/<int:id>', methods=['GET'])
@login_required
def toggle_comment_status(id):
    report = VisitReport.query.get_or_404(id)
    report.status = 0 if report.status == 1 else 1
    db.session.commit()
    flash('评论状态已更新！')
    
    referer = request.headers.get('Referer', '')
    if referer and 'status=0' in referer:
        return redirect(url_for('manage.comments', status=0))
    elif referer and 'status=2' in referer:
        return redirect(url_for('manage.comments', status=2))
    return redirect(url_for('manage.comments'))

@bp.route('/comment/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_comment(id):
    report = VisitReport.query.get_or_404(id)
    
    if request.method == 'POST':
        report.content = request.form['content']
        
        try:
            db.session.commit()
            flash('评论编辑成功！')
            return redirect(url_for('manage.comments'))
        except Exception as e:
            db.session.rollback()
            flash(f'编辑失败：{str(e)}', 'error')
    
    return render_template('manage/comment_form.html', comment=report)

@bp.route('/comment/delete/<int:id>', methods=['GET'])
@login_required
def delete_comment(id):
    report = VisitReport.query.get_or_404(id)
    try:
        db.session.delete(report)
        db.session.commit()
        flash('评论删除成功！')
    except Exception as e:
        db.session.rollback()
        flash(f'删除失败：{str(e)}', 'error')
    
    return redirect(url_for('manage.comments'))