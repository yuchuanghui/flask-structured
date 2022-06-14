from flask_httpauth import HTTPBasicAuth
from ..models import User
from flask import g, make_response, jsonify, render_template
from .errors import forbidden, unauthorized
from . import api

auth = HTTPBasicAuth(scheme='fuck', realm=None)

@api.before_request
@auth.login_required
def before_request():
    if not g.current_user.is_anonymous and not g.current_user.confirmed:
        return forbidden('Unconfirmed account')

@auth.error_handler
def auth_error():
    return unauthorized('Invalid credentials')

@auth.verify_password
def verify_password(username_or_token, password):
    if username_or_token == '':
        return False
    if password == '':
        g.current_user = User.verify_auth_token(username_or_token)
        g.token_used = True
        return g.current_user is not None
    user = User.query.filter(User.username == username_or_token).first()
    if not user:
        return False
    g.current_user = user
    g.token_used = False
    return user.verify_password(password)

@api.route('/api/login', methods=['POST'])
def login():
    token = g.current_user.generate_auth_token(expiration=3600)
    data = g.current_user.to_json()
    rsp = make_response(jsonify({'data': data}))
    rsp.headers['authorization'] = token
    return rsp
