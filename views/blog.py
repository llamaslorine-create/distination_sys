from flask import Blueprint, request, render_template, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from models.BlogPost import BlogPost, BlogComment
from db import db
from utils.oss_utils import oss_manager
from config import OSS_BLOG_IMAGE_DIR

bp = Blueprint('blog', __name__, url_prefix='/blog')

@bp.route('/', methods=['GET'])
@login_required
def index():
    """博客首页 - 博文列表"""
    page = request.args.get('page', 1, type=int)
    
    is_admin = current_user.is_authenticated and hasattr(current_user, 'is_admin') and current_user.is_admin
    
    if is_admin:
        pagination = BlogPost.query.order_by(BlogPost.create_time.desc()).paginate(page=page, per_page=10)
        return render_template('blog/admin_list.html', posts=pagination.items, pagination=pagination)
    else:
        pagination = BlogPost.query.filter_by(status=1).order_by(BlogPost.create_time.desc()).paginate(page=page, per_page=10)
        return render_template('blog/list.html', posts=pagination.items, pagination=pagination)

@bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    """发表旅游博文"""
    is_admin = current_user.is_authenticated and hasattr(current_user, 'is_admin') and current_user.is_admin
    
    if request.method == 'POST':
        author_name = request.form['author_name']
        title = request.form['title']
        content = request.form['content']
        
        if not author_name or not title or not content:
            flash('请填写完整信息', 'error')
            return render_template('blog/add.html')
        
        try:
            post = BlogPost(
                author_name=author_name,
                title=title,
                content=content
            )
            
            if 'image' in request.files:
                file = request.files['image']
                if file and file.filename:
                    image_url, error = oss_manager.upload_file(file, OSS_BLOG_IMAGE_DIR)
                    if image_url:
                        post.image_url = image_url

            db.session.add(post)
            db.session.commit()
            
            flash('博文发表成功！')
            return redirect(url_for('blog.index'))
        except Exception as e:
            db.session.rollback()
            flash(f'发表失败: {str(e)}', 'error')
    
    if is_admin:
        return render_template('blog/admin_add.html')
    else:
        return render_template('blog/add.html')

@bp.route('/edit/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit(post_id):
    """编辑博文"""
    post = BlogPost.query.get_or_404(post_id)
    
    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        post.author_name = request.form['author_name']
        
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename:
                image_url, error = oss_manager.upload_file(file, OSS_BLOG_IMAGE_DIR)
                if image_url:
                    post.image_url = image_url
        
        try:
            db.session.commit()
            flash('博文更新成功！')
            return redirect(url_for('blog.view', post_id=post.post_id))
        except Exception as e:
            db.session.rollback()
            flash(f'更新失败: {str(e)}', 'error')
    
    return render_template('blog/edit.html', post=post)

@bp.route('/view/<int:post_id>', methods=['GET'])
@login_required
def view(post_id):
    """查看博文详情"""
    post = BlogPost.query.get_or_404(post_id)
    
    post.view_count += 1
    db.session.commit()
    
    is_admin = current_user.is_authenticated and hasattr(current_user, 'is_admin') and current_user.is_admin
    
    if is_admin:
        return render_template('blog/admin_view.html', post=post)
    else:
        return render_template('blog/view.html', post=post)

@bp.route('/comment/<int:post_id>', methods=['POST'])
def comment(post_id):
    """发表评论或回复"""
    author_name = request.form['author_name']
    content = request.form['content']
    parent_id = request.form.get('parent_id', type=int)
    
    if not author_name or not content:
        flash('请填写完整信息', 'error')
        return redirect(url_for('blog.view', post_id=post_id))
    
    try:
        comment = BlogComment(
            post_id=post_id,
            parent_id=parent_id,
            author_name=author_name,
            content=content
        )
        db.session.add(comment)
        db.session.commit()
        
        flash('评论发表成功！')
    except Exception as e:
        db.session.rollback()
        flash(f'评论失败: {str(e)}', 'error')
    
    return redirect(url_for('blog.view', post_id=post_id))

@bp.route('/delete/<int:post_id>', methods=['GET'])
@login_required
def delete(post_id):
    """删除博文"""
    post = BlogPost.query.get_or_404(post_id)
    
    try:
        db.session.delete(post)
        db.session.commit()
        flash('博文删除成功！')
    except Exception as e:
        db.session.rollback()
        flash(f'删除失败: {str(e)}', 'error')
    
    return redirect(url_for('blog.index'))
