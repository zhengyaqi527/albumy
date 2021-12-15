import os


basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


class Operations:
    CONFIRM = 'confirm'
    RESET_PASSWORD = 'reset-password'
    CHANGE_EMAIL = 'change-email'


class BaseConfig:

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY')

    MAX_CONTENT_LENGTH = 3 * 1024 * 1024

    # 邮件发送
    ALBUMY_ADMIN_EMAIL = os.environ.get('ALBUMY_ADMIN', 'yaqi.zheng@guokr.com')
    ALBUMY_MAIL_SUBJECT_PREFIX = '[Albumy]'

    # 邮件服务器配置
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('Albumy Admin', MAIL_USERNAME)

    # 图片上传设置
    DROPZONE_MAX_FILE_SIZE = 3
    DROPZONE_MAX_FILES = 30
    DROPZONE_ALLOWED_FILE_TYPE = 'image'
    DROPZONE_ENABLE_CSRF = True

    # 图片上传
    ALBUMY_UPLOAD_PATH = os.path.join(basedir, 'uploads')
    ALBUMY_PHOTO_SIZE = {'small': 400, 'medium': 800}
    ALBUMY_PHOTO_SUFFIX = {
        ALBUMY_PHOTO_SIZE['small']: '_s', 
        ALBUMY_PHOTO_SIZE['medium']: '_m'
    }

    # 头像设置
    AVATARS_SAVE_PATH = os.path.join(ALBUMY_UPLOAD_PATH, 'avatars')
    AVATARS_SIZE_TUPLE = (30, 100, 200)

    # 前台数据显示
    ALBUMY_PHOTO_PER_PAGE = 12
    ALBUMY_USER_PER_PAGE = 12
    ALBUMY_COMMENT_PER_PAGE = 12
    ALBUMY_USER_PER_PAGE = 12
    ALBUMY_NOTIFICATION_PER_PAGE = 12
    
    # 管理后台列表展示
    ALBUMY_MANAGE_USER_PER_PAGE = 20
    ALBUMY_MANAGE_PHOTO_PER_PAGE = 20
    ALBUMY_MANAGE_TAG_PER_PAGE = 20
    ALBUMY_MANAGE_COMMENT_PER_PAGE = 20


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    

class TestingConfig(BaseConfig):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}