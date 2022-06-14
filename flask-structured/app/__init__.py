# 用于注册app、插件等

from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_login import LoginManager
from flask_pagedown import PageDown
from flask_admin.contrib.sqla import ModelView
from app.my_admin_class import MyAdmin, MyAdminIndexView

bootstrap = Bootstrap5()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
pagedown = PageDown()
admin = MyAdmin(name='Fuck', template_mode='bootstrap4')

login_manager = LoginManager()
login_manager.login_view = 'auth.login'  # 匿名用户会被重定向至该蓝图页面

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)  # 注册静态方法

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    pagedown.init_app(app)
    admin.init_app(app, index_view=MyAdminIndexView())

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, prefix='api')

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, prefix='auth')

    from .admin_bp import admin_bp as admin_blueprint
    app.register_blueprint(admin_blueprint, prefix='admin')

    from app.models import User, Role, Post, Permission, Comment, Follow
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Post, db.session))
    admin.add_view(ModelView(Role, db.session))
    admin.add_view(ModelView(Comment, db.session))
    admin.add_view(ModelView(Follow, db.session))

    # define routes and custom error pages

    return app
