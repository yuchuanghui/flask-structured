from flask import Blueprint

# 注册蓝图

main = Blueprint('main', __name__)
auth = Blueprint('auth', __name__)

from . import views, errors

