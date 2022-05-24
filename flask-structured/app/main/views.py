from datetime import datetime
from flask import render_template, session, redirect, url_for, current_app, request, abort, flash, make_response
from . import main
from .forms import NameForm, PostForm
from .. import db
from ..models import User, Permission, Post, Follow
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
    show_followed = False
    # avatar = show_avatar('get', current_user.avatar)
    # avatar = "data:image/jpg;base64," + str(base64.b64encode(avatar))[2: -1]
    if current_user.can(Permission.WRITE) and form.validate_on_submit():
        post = Post(body=form.body.data, author=current_user._get_current_object())
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('main.index'))
    if current_user.is_authenticated:
        show_followed = bool(request.cookies.get('show_followed', ''))
    if show_followed:
        query = current_user.followed_posts
    else:
        print('Post')
        query = Post.query

    page = request.args.get('page', 1, type=int)  # 获取get请求中的UrlParams
    pagination = query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE']
    )
    posts = pagination.items
    print(show_followed)
    return render_template('index.html', posts=posts, form=form, current_time=datetime.utcnow(), pagination=pagination, show_followed=show_followed)

    # return render_template('index.html',
    #                        form=form,
    #                        name=session.get('name'),
    #                        known=session.get('known', False),
    #                        current_time=datetime.utcnow())
@main.route('/all')
@login_required
def show_all():
    resp = make_response(redirect(url_for('main.index')))
    resp.set_cookie('show_followed', '', max_age=30 * 24 * 60 * 60)
    return resp

@main.route('/followed')
@login_required
def show_followed():
    resp = make_response(redirect(url_for('main.index')))
    resp.set_cookie('show_followed', '1', max_age=30 * 24 * 60 * 60)
    return resp

@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = user.posts.order_by(Post.timestamp.desc()).all()
    avatar = user.show_my_avatar()
    return render_template('user.html', user=user, avatar=avatar, posts=posts)

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

# @main.route('/admin')
# @login_required
# @admin_reqired
# def for_admins_only():
#     return "For administrators"

@main.route('/follow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User does not exist')
        return redirect(url_for('main.index'))
    elif current_user.is_following(user):
        flash(f'You have followed {username}')
        return redirect(url_for('main.user', username=user.username))
    else:
        current_user.follow(user)
        db.session.commit()
        flash(f'You are now following {username}')
        return redirect(url_for('main.user', username=user.username))

@main.route('/unfollow/<username>')
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User does not exist')
        return redirect(url_for('main.index'))
    elif current_user.is_following(user):
        current_user.unfollow(user)
        db.session.commit()
        flash(f'You have unfollowed {username}')
        return redirect(url_for('main.user', username=user.username))
    else:
        flash(f'You have not followed {username}')
        return redirect(url_for('main.user', username=user.username))

@main.route('/follow-list/<username>/<tag>')
def follow_list(username, tag):
    user = User.query.filter_by(username=username).first()
    page = request.args.get('page', 1, type=int)
    if tag == 'fan':
        pagination = user.fan.order_by(Follow.timestamp.desc()).paginate(page, per_page=current_app.config['FLASKY_FOLLOWERS_PER_PAGE'])
        follows = [{'user': item.fan.username, 'time': item.timestamp} for item in pagination.items]
    elif tag == 'up':
        pagination = user.up.paginate(page, per_page=current_app.config['FLASKY_FOLLOWERS_PER_PAGE'])
        follows = [{'user': item.up.username, 'time': item.timestamp} for item in pagination.items]
    else:
        redirect(url_for('main.user', username=user.username))
    return render_template('follow_list.html', follows=follows, pagination=pagination, user=user, endpoint='.follow_list', tag=tag)

@main.route('/moderate')
@login_required
@permission_required(Permission.MODERATE)
def for_moderators_only():
    return "For administrators"
