# 错误处理页面

from flask import render_template
from . import main

@main.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@main.app_errorhandler(500)  # 使用app_error handle,对全局错误响应
def internal_server_error(e):
    return render_template('500.html'), 500
