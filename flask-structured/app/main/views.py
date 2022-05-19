from datetime import datetime
from flask import render_template, session, redirect, url_for, current_app, request, abort, flash
from . import main
from .forms import NameForm, PostForm
from .. import db
from ..models import User, Permission, Post
from flask_login import login_required, current_user
from ..decorators import admin_reqired, permission_required
import base64

@main.route('/', methods=['GET', 'POST'])
def index():
    # form = NameForm()
    # if form.validate_on_submit():
    #     username = User.query.filter_by(username=form.name.data).first()
    #     if username is None:
    #         user = User(username=form.name.data)
    #         # if app.config['FLASKY_ADMIN']:
    #         #     send_email(app.config['FLASKY_ADMIN'], 'New User')
    #         db.session.add(user)
    #         db.session.commit()
    #         session['name'] = form.name.data
    #         session['known'] = False

    #     else:
    #         session['known'] = True
    #         # form.name.data = ''
    #     session['name'] = form.name.data
    #     return redirect(url_for('.index'))
    form = PostForm()
    # avatar = show_avatar('get', current_user.avatar)
    # avatar = "data:image/jpg;base64," + str(base64.b64encode(avatar))[2: -1]
    if current_user.can(Permission.WRITE) and form.validate_on_submit():
        post = Post(body=form.body.data, author=current_user._get_current_object())
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('main.index'))
    page = request.args.get('page', 1, type=int)  # 获取get请求中的UrlParams
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE']
    )
    posts = pagination.items
    return render_template('index.html', posts=posts, form=form, current_time=datetime.utcnow(), pagination=pagination)

    # return render_template('index.html',
    #                        form=form,
    #                        name=session.get('name'),
    #                        known=session.get('known', False),
    #                        current_time=datetime.utcnow())

@main.route('/post/<int:id>')
def post(id):
    post = Post.query.get_or_404(id)
    return render_template('post.html', posts=[post])

@main.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    post = Post.query.get_or_404(id)
    if current_user != post.author and not current_user.can(Permission.ADMIN):
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.body = form.body.data
        db.session.add(post)
        db.session.commit()
        flash('The psot has been updated')
        return redirect(url_for('main.post', id=post.id))
    form.body.data = post.body
    return render_template('edit_post.html', form=form)

@main.route('/admin')
@login_required
@admin_reqired
def for_admins_only():
    return "For administrators"

@main.route('/moderate')
@login_required
@permission_required(Permission.MODERATE)
def for_moderators_only():
    return "For administrators"

