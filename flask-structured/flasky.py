import os
from app import create_app, db
from app.models import User, Role, Post, Permission
from flask_migrate import Migrate

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db, render_as_batch=True)

@app.context_processor
def include_permissions_class():
    return dict(Permission=Permission)

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role, Post=Post, Permission=Permission)


@app.cli.command()
def test():  # 命令行唤起测试时使用的名字 flask test
    """Run the unit tests"""
    import unittest
    tests = unittest.TestLoader().discover("tests")
    unittest.TextTestRunner(verbosity=2).run(tests)
