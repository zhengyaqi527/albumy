from flask import url_for

from albumy.extensions import db
from albumy.models import Notification


# 被关注通知
def push_follow_notification(follower, receiver):
    message = 'User <a href="%s">%s</a> followed you.' % (url_for('user.index', username=follower.username), follower.username)
    notification = Notification(message=message, receiver=receiver)
    db.session.add(notification)
    db.session.commit()


# 收到评论或回复通知
def push_comment_notification(photo_id, receiver, page=1):
    message = '<a href="%s#comments">This photo</a> has new comment/reply.' % (url_for('mian.show_photo', photo_id=photo_id, page=page))
    notification = Notification(message=message, receiver=receiver)
    db.session.add(notification)
    db.session.commit()


# 照片被收藏通知
def push_collect_notification(collector, photo_id, receiver):
    message = 'User <a href="%s">%s</a> collected your <a href="%s">photo</a>' % (\
                url_for('user.index', username=collector.username),
                collector.username,
                url_for('main.show_photo', photo_id=photo_id)
        )
    notification = Notification(message=message, receiver=receiver)
    db.session.add(notification)
    db.session.commit()
                
                