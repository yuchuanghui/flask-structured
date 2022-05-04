from datetime import datetime
from flask import render_template, session, redirect, url_for
from . import main
from .forms import NameForm
from .. import db
from ..models import User, Permission
from flask_login import login_required
from ..decorators import admin_reqired, permission_required
import requests
import base64


@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        username = User.query.filter_by(username=form.name.data).first()
        if username is None:
            user = User(username=form.name.data)
            # if app.config['FLASKY_ADMIN']:
            #     send_email(app.config['FLASKY_ADMIN'], 'New User')
            db.session.add(user)
            db.session.commit()
            session['name'] = form.name.data
            session['known'] = False

        else:
            session['known'] = True
            # form.name.data = ''
        session['name'] = form.name.data
        return redirect(url_for('.index'))
    return render_template('index.html',
                           form=form,
                           name=session.get('name'),
                           known=session.get('known', False),
                           current_time=datetime.utcnow())

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

@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    headers = {"Authorization": "q-sign-algorithm=sha1&q-ak=AKIDrXx63j8G7i24pKcePu74j7E4dvxiCPM2&q-sign-time=1650951782;1650955382&q-key-time=1650951782;1650955382&q-header-list=&q-url-param-list=&q-signature=8ce539628edcfc5ef9cf2270079b5ff9ded40408"}
    avatar = requests.get("https://flask-media-1305646899.cos.ap-beijing.myqcloud.com/bird.png", headers=headers)
    return render_template('user.html', user=user, avatar="data:image/jpg;base64," + str(base64.b64encode(avatar.content))[2: -1])
