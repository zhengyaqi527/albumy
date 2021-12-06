from flask import Blueprint, render_template, request, current_app, flash, redirect
from flask.helpers import url_for
from flask_login import login_required, current_user

from albumy.models import Photo, User, Collect
from albumy.decorators import confirm_required, permission_requeired
from albumy.utils import redirect_back
from albumy.notifications import push_follow_notification

user_bp = Blueprint('user', __name__)


# 用户主页
@user_bp.route('/<username>')
def index(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['ALBUMY_PHOTO_PER_PAGE']
    pagination = Photo.query.with_parent(user).order_by(Photo.timestamp.desc()).paginate(page, per_page, error_out=False)
    photos = pagination.items
    return render_template('user/index.html', user=user, photos=photos, pagination=pagination)


# 展示用户收藏内容
@user_bp.route('/<username>/collections')
def show_collections(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['ALBUMY_PHOTO_PER_PAGE']
    pagination = Collect.query.with_parent(user).order_by(Collect.timestamp.desc()).paginate(page, per_page, error_out=False)
    collects = pagination.items
    return render_template('user/collections.html', user=user, pagination=pagination, collects=collects)


# 关注（有关注权限的才能进行关注）
@user_bp.route('/follow/<username>', methods=['POST'])
@login_required
@confirm_required
@permission_requeired('FOLLOW')
def follow(username):
    user = User.query.filter_by(username=username).first_or_404()
    if current_user.is_following(user):
        flash('Already followed.', 'info')
        return redirect(url_for('.index', username=username))
    current_user.follow(user)
    flash('User followed.', 'info')
    push_follow_notification(follower=current_user, receiver=user)
    return redirect_back()


# 取消关注
@user_bp.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first_or_404()
    if not current_user.is_following(user):
        flash('Not follow yet.', 'info')
        return redirect(url_for('.index', username=username))
    current_user.unfollow(user)
    flash('User unfollowed.', 'info')
    return redirect_back()


# 显示关注当前用户的人
@user_bp.route('/<username>/followers')
def show_followers(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['ALBUMY_USER_PER_PAGE']
    pagination = user.followers.paginate(page, per_page, error_out=False)
    follows = pagination.items
    return render_template('user/followers.html', follows=follows, pagination=pagination, user=user)


# 显示当前用户关注的人
@user_bp.route('/<username>/following')
def show_following(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['ALBUMY_USER_PER_PAGE']
    pagination = user.following.paginate(page, per_page, error_out=False)
    follows = pagination.items
    return render_template('user/following.html', follows=follows, pagination=pagination, user=user)