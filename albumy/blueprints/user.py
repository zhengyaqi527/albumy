from flask import Blueprint, render_template, request,current_app

from albumy.models import Photo, User, Collect

user_bp = Blueprint('user', __name__)


@user_bp.route('/<username>')
def index(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['ALBUMY_PHOTO_PER_PAGE']
    pagination = Photo.query.with_parent(user).order_by(Photo.timestamp.desc()).paginate(page, per_page, error_out=False)
    photos = pagination.items
    return render_template('user/index.html', user=user, photos=photos, pagination=pagination)


@user_bp.route('/<username>/collections')
def show_collections(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['ALBUMY_PHOTO_PER_PAGE']
    pagination = Collect.query.with_parent(user).order_by(Collect.timestamp.desc).pagination(page, per_page, error_out=False)
    collects = pagination.items
    return render_template('user/collections.html', user=user, pagination=pagination, collects=collects)