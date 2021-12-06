from flask import Blueprint, render_template, jsonify
from  flask_login import current_user

from albumy.models import Notification, User

ajax_bp = Blueprint('ajax', __name__)


# 获取用户资料
@ajax_bp.route('/profile/<int:user_id>')
def get_profile(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('main/profile_popup.html', user=user)


# 关注者数量
@ajax_bp.route('/followers-count/<int:user_id>')
def followers_count(user_id):
    user = User.query.get_or_404(user_id)
    count = user.followers.count() - 1
    return jsonify(count=count)


# 关注、取消关注
@ajax_bp.route('/follow/<username>', methods=['POST'])
def follow(username):
    if not current_user.is_authenticated():
        return jsonify(message='Login required.'), 403

    if not current_user.confirmed():
        return jsonify(message='Confirm account required.'), 400

    if not current_user.can('FOLLOW'):
        return jsonify(message='No permission.'), 403
    
    user = User.query.filter_by(username=username).first_or_404()
    if current_user.is_following(user):
        return jsonify(mesage='Already followed.'), 400
    
    current_user.follow(user)
    return jsonify(message='User followed.')


@ajax_bp.route('/unfollow/<username>')
def unfollow(username):
    if not current_user.is_authenticated():
        return jsonify(message='Login required.'), 403
    
    user = User.query.filter_by(username=username).first_or_404()
    if not current_user.is_following(user):
        return jsonify(mesage='Not follow yet.'), 400
    
    current_user.unfollow(user)
    return jsonify(message='Follow canceled.')


# 获取通知数量
@ajax_bp.route('/notifications-count')
def notifications_count():
    if not current_user.is_authenticated:
        return jsonify(message='Login required'), 403
    
    count = Notification.query.with_parent(current_user).filter_by(is_read=False).count()
    return jsonify(count=count)