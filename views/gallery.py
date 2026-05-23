from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from flask_login import login_required, current_user
from utils.oss_utils import oss_manager
from config import ALLOWED_EXTENSIONS, MAX_FILE_SIZE
import os

bp = Blueprint('gallery', __name__, url_prefix='/gallery')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/')
@login_required
def index():
    return render_template('gallery/index.html')

@bp.route('/upload', methods=['POST'])
@login_required
def upload():
    if 'file' not in request.files:
        return jsonify({'status': 'error', 'message': '没有选择文件'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'status': 'error', 'message': '文件名不能为空'})
    
    if not allowed_file(file.filename):
        return jsonify({'status': 'error', 'message': '不支持的文件格式'})
    
    content_type = request.form.get('content_type', 'general')
    directory_map = {
        'avatar': 'avatars/',
        'spot': 'spot_images/',
        'report': 'report_images/',
        'route': 'route_covers/',
        'blog': 'blog_images/',
        'announcement': 'announcement_images/'
    }
    directory = directory_map.get(content_type, '')
    
    file_url, error = oss_manager.upload_file(file, directory)
    
    if error:
        return jsonify({'status': 'error', 'message': error})
    
    return jsonify({
        'status': 'success',
        'message': '上传成功',
        'url': file_url
    })

@bp.route('/batch_upload', methods=['POST'])
@login_required
def batch_upload():
    if 'files' not in request.files:
        return jsonify({'status': 'error', 'message': '没有选择文件'})
    
    files = request.files.getlist('files')
    content_type = request.form.get('content_type', 'general')
    directory_map = {
        'avatar': 'avatars/',
        'spot': 'spot_images/',
        'report': 'report_images/',
        'route': 'route_covers/',
        'blog': 'blog_images/',
        'announcement': 'announcement_images/'
    }
    directory = directory_map.get(content_type, '')
    
    results = []
    for file in files:
        if file.filename == '':
            continue
        
        if not allowed_file(file.filename):
            results.append({'filename': file.filename, 'status': 'error', 'message': '不支持的文件格式'})
            continue
        
        file_url, error = oss_manager.upload_file(file, directory)
        
        if error:
            results.append({'filename': file.filename, 'status': 'error', 'message': error})
        else:
            results.append({'filename': file.filename, 'status': 'success', 'url': file_url})
    
    success_count = sum(1 for r in results if r['status'] == 'success')
    return jsonify({
        'status': 'success' if success_count > 0 else 'error',
        'message': f'成功上传 {success_count}/{len(results)} 个文件',
        'results': results
    })

@bp.route('/delete', methods=['POST'])
@login_required
def delete():
    file_url = request.form.get('url')
    if not file_url:
        return jsonify({'status': 'error', 'message': '文件URL不能为空'})
    
    success = oss_manager.delete_file(file_url)
    
    if success:
        return jsonify({'status': 'success', 'message': '删除成功'})
    else:
        return jsonify({'status': 'error', 'message': '删除失败'})