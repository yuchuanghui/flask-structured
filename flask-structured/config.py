import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'yisiyuhui'
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'stmp.163.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', '25'))  # 邮件端口
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower()
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = 'Flasky Admin <flask-ych@163.com>'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    SQLALCHEMY_TRACKMODIFICATIONS = False
    # SECRET_KEY = 'yisiyuhui'
    # MAIL_SERVER = 'smtp.163.com'
    # MAIL_PORT = 25  # 邮件端口
    # MAIL_USE_TLS = True
    # MAIL_USE_SSL = False
    # MAIL_USERNAME = 'flask_ych@163.com'
    # MAIL_PASSWORD = 'QONNFKCSOOONDEYC'
    # FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    # FLASKY_MAIL_SENDER = 'Flasky Admin <flask_ych@163.com>'
    # FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    # SQLALCHEMY_TRACKMODIFICATIONS = False
    MAX_CONTENT_LENGTH = 1 * 1024 * 1024
    FLASKY_POSTS_PER_PAGE = 5
    FLASKY_FOLLOWERS_PER_PAGE = 10
    
    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'data.dev.sqlite')

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'sqlite://'

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.environ.get(basedir, 'data.sqlite')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
