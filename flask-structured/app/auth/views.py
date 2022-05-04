from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from . import auth
from .forms import LoginForm, RegistrationForm, ChangePasswordForm, ResetPasswordForm, SendResetMailForm, EditProfileForm
from ..models import User
from .. import db
from ..email import send_mail
from time import sleep


@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.confirmed and request.blueprint != 'auth' and request.endpoint != 'static':
            return redirect(url_for('auth.unconfirmed'))


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            next = request.args.get('next')  # 重定向回到原来的页面
            if next is None or not next.startswith('/'):
                next = url_for('main.index')
            return redirect(next)
        flash('Invalid username or password')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_mail(user.email, 'Confirm Your Account', 'auth/email/confirm', user=user, token=token)
        login_user(user)
        return redirect(url_for('auth.unconfirmed'))
    return render_template('auth/register.html', form=form)


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('auth.confirmed'))
    if current_user.confirm(token):
        db.session.commit()
        flash('You have confirm you account')
        return redirect(url_for('auth.confirmed'))
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('auth.unconfirmed'))


@auth.route('/resend')
@login_required
def resend():
    token = current_user.generate_confirmation_token()
    send_mail(current_user.email,
              'Confirm Your Account',
              'auth/email/confirm',
              user=current_user,
              token=token)
    flash('A new email has been sent.')
    return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed')
@login_required
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('auth.confirmed'))
    return render_template('auth/unconfirmed.html')


@auth.route('/confirmed')
def confirmed():
    return render_template('auth/jump.html')


@auth.route('/changepassword', methods=['GET', 'POST'])
@login_required
def changepassword():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        user = current_user
        if user.verify_password(form.current_password.data):
            user.change_password(form.new_password.data)
            db.session.commit()
            return redirect(url_for('auth.confirmed'))
        else:
            flash('Password is incorrect. Please try again.')
            return redirect(url_for('auth.changepassword'))
    return render_template('auth/ch_password.html', form=form)


@auth.route('/sendresetmail', methods=['GET', 'POST'])
def sendresetmail():
    form = SendResetMailForm()
    user = User.query.filter_by(email=form.email.data).first()
    if form.validate_on_submit():
        token = user.generate_confirmation_token()
        send_mail(user.email,
                  'Confirm Your Account',
                  'auth/email/resetpassword',
                  user=user,
                  token=token)
        return redirect(url_for('auth.confirmed'))
    return render_template('auth/sendresetmail.html', form=form)


@auth.route('/resetpassword/<token>/<email>', methods=['GET', 'POST'])
def resetpassword(token, email):
    form = ResetPasswordForm()
    user = User.query.filter_by(email=email).first()
    if form.validate_on_submit():
        if user.confirm(token):
            user.change_password(form.password.data)
            db.session.commit()
            login_user(user)
            flash('complete')
            return redirect(url_for('auth.confirmed'))
        else:
            flash('token has expired or wrong. Please resend a email.')
            redirect(url_for('auth.sendresetemail'))
    return render_template('auth/resetpassword.html', form=form)

@auth.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user._get_current_object())
        db.session.commit()
        flash('You profile have been updated.')
        return redirect(url_for('main.user', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.location.about_me = current_user.about_me
    return render_template('auth/edit_profile.html', form=form)
