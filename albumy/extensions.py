from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, AnonymousUserMixin
from flask_moment import Moment
from flask_dropzone import Dropzone
from flask_avatars import Avatars
from flask_wtf import CSRFProtect


db = SQLAlchemy()
migrate = Migrate()
mail = Mail()
bootstrap = Bootstrap()
login_manager = LoginManager()
moment = Moment()
dropzone = Dropzone()
avatars = Avatars()
csrf = CSRFProtect()


@login_manager.user_loader
def load_user(user_id):
    from albumy.models import User
    user = User.query.get(int(user_id))
    return user


# 设置登录视图的端点及信息分类
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'warning'

# 设置重新认证视图的端点及信息分类
login_manager.refresh_view = 'auth.re_authenticate'
login_manager.needs_refresh_message_category = 'warning'


class Guest(AnonymousUserMixin):
    def can(self, permission_name):
        return False

    @property
    def is_admin(self):
        return False

login_manager.anonymous_user = Guest