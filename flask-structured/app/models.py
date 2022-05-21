from flask_login import current_user
from flask import redirect, url_for, flash
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from . import login_manager
from flask_login import UserMixin, AnonymousUserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from datetime import datetime
from .avatar import show_avatar, upload_avatar
from base64 import b64encode
from markdown import markdown
import bleach
from flask_admin.contrib.sqla import ModelView

# 注册数据库对象

class Role(db.Model):
    # 相当于创造多个Role对象，每个Role对象对应一个roles表格中的一项
    __tablename__ = 'roles'  # 定义表格名，在建立关系时使用
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship(
        'User', backref='role',
        lazy='dynamic')  # 此时已经通过id将两个model连起来了，现在将users属性指向User model， backref为User提供一个可以反向访问Role的属性

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

    def __repr__(self):
        return '<Role %r>' % self.name  # formate格式

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm

    def reset_permissions(self):
        self.permissions = 0

    def has_permission(self, perm):
        return self.permissions & perm == perm

    @staticmethod
    def insert_roles():
        roles = {
            'User': [Permission.FOLLOW, Permission.COMMENT, Permission.WRITE],
            'Moderator': [Permission.FOLLOW, Permission.COMMENT, Permission.WRITE, Permission.MODERATE],
            'Administrator': [Permission.FOLLOW, Permission.COMMENT, Permission.WRITE, Permission.MODERATE, Permission.ADMIN]
        }
        default_role = 'User'
        for r in Role.query.all():
            if r.name not in roles.keys():
                db.session.delete(r)
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.reset_permissions()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default = (role.name == default_role)
            db.session.add(role)
        db.session.commit()


class Permission():
    FOLLOW = 1
    COMMENT = 2
    WRITE = 4
    MODERATE = 8
    ADMIN = 16


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"))  # 创建一个ForeignKey， 被识别为role的id
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    name = db.Column(db.String(64))
    location = db.Column(db.String(64))
    about_me = db.Column(db.Text())
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)
    avatar = db.Column(db.String(), default='/bird.png')
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['FLASKY_ADMIN']:
                self.role = Role.query.filter_by(name='Administrator').first()
            else:
                self.role = Role.query.filter_by(default=True).first()

    def __repr__(self):
        return '<User %r>' % self.email

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def change_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id}).decode('utf-8')

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except (TypeError, ValueError):
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def can(self, perm):
        return self.role is not None and self.role.has_permission(perm)

    def is_administrator(self):
        return self.can(Permission.ADMIN)

    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    def show_my_avatar(self):
        if self.avatar is None:
            self.avatar = '/bird.png'
        avatar_bytes = show_avatar('get', self.avatar)
        avatar = "data:image/jpg;base64," + str(b64encode(avatar_bytes))[2: -1]
        return avatar

    def upload_my_avatar(self, avatar):
        filename = self.username + avatar.filename[-4:]
        upload_avatar(filename, avatar, avatar.mimetype)
        return '/' + filename


class AnonymousUser(AnonymousUserMixin):
    def can(self, perm):
        return False

    def is_administrator(self):
        return False


login_manager.anonymous_user = AnonymousUser  # 告诉login_manager默认的匿名用户是上面定义的

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text())
    body_html = db.Column(db.Text())
    timestamp = db.Column(db.DateTime(), index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code', 'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul', 'h1', 'h2', 'h3', 'p']
        # target.body_html = bleach.linkify(bleach.clean(
        #     markdown(value, extensions=['md4mathjax'], output_format='html'),
        #      strip=True
        # ))
        target.body_html = bleach.linkify(markdown(value, extensions=['md4mathjax'], output_format='html'))


db.event.listen(Post.body, 'set', Post.on_changed_body)