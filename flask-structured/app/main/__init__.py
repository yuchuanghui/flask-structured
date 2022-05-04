from flask import Blueprint
from ..models import Permission

# 注册蓝图

main = Blueprint('main', __name__)
auth = Blueprint('auth', __name__)

@main.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)


from . import views, errors

