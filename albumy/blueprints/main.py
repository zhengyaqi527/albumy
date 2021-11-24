import os

from flask import Blueprint, render_template, request, current_app, send_from_directory, flash
from flask.helpers import url_for
from flask_dropzone import random_filename
from flask_login import login_required, current_user
from werkzeug.utils import redirect

from albumy.extensions import db
from albumy.decorators import permission_requeired, confirm_required
from albumy.models import Photo
from albumy.utils import resize_image


main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    return render_template('main/index.html')


@main_bp.route('/explore')
def explore():
    return render_template('main/explore.html')


@main_bp.route('/avatars/<path:filename>')
def get_avatar(filename):
    return send_from_directory(current_app.config['AVATARS_SAVE_PATH'], filename)


@main_bp.route('/uploads/<path:filename>')
def get_image(filename):
    return send_from_directory(current_app.config['ALBUMY_UPLOAD_PATH'], filename)


@main_bp.route('/upload', methods=['GET', 'POST'])
@login_required
@confirm_required
@permission_requeired('UPLOAD')
def upload():
    if request.method == 'POST' and 'file' in request.files:
        f = request.files.get('file') # 获取图片对象
        filename = random_filename(f.filename) # 生成随机文件名
        f.save(os.path.join(current_app.config['ALBUMY_UPLOAD_PATH'], filename)) # 保存文件对象
        filename_s = resize_image(f, filename, current_app.config['ALBUMY_PHOTO_SIZE']['small'])
        filename_m = resize_image(f, filename, current_app.config['ALBUMY_PHOTO_SIZE']['medium'])
        photo = Photo(
            filename=filename,
            filename_s=filename_s,
            filename_m=filename_m,
            author=current_user._get_current_object()
        )
        db.session.add(photo)
        db.session.commit()
    
    return render_template('main/upload.html')


@main_bp.route('/photo/<int:photo_id>')
def show_photo(photo_id):
    photo = Photo.query.get_or_404(photo_id)
    return render_template('main/photo.html', photo=photo)


@main_bp.route('/photo/next/<int:photo_id>')
def photo_next(photo_id):
    photo = Photo.query.get_of_404(photo_id)
    photo_n = Photo.query.query.with_parent(photo.author).filter(Photo.id < photo_id).order_by(Photo.id.desc()).first()
    if photo_n is None:
        flash('This is already the last one.', 'info')
        return redirect(url_for('show_photo', photo_id=photo_id))
    return redirect(url_for('.show_photo', photo_id=photo_n.id))


@main_bp.route('/photo/pre/<int:photo_id>')
def photo_previous(photo_id):
    photo = Photo.query.get_of_404(photo_id)
    photo_p = Photo.query.query.with_parent(photo.author).filter(Photo.id > photo_id).order_by(Photo.id.asc()).first()
    if photo_p is None:
        flash('This is already the first one.', 'info')
        return redirect(url_for('show_photo', photo_id=photo_id))    
    return redirect(url_for('.show_photo', photo_id=photo_p.id))    