# admin_blueprint
from flask import redirect, url_for, flash
from flask_admin import Admin, AdminIndexView
from flask_admin.menu import MenuView
from flask_login import current_user
from flask_admin import babel

class MyAdminIndexView(AdminIndexView):

    def __init__(self, name=None, category=None,
                 endpoint=None, url=None,
                 template='admin/index.html',
                 menu_class_name=None,
                 menu_icon_type=None,
                 menu_icon_value=None):
        super(MyAdminIndexView, self).__init__(name or babel.lazy_gettext('Home'),
                                               category,
                                               endpoint or 'admin',
                                               '/admin' if url is None else url,
                                               'static',
                                               menu_class_name=menu_class_name,
                                               menu_icon_type=menu_icon_type,
                                               menu_icon_value=menu_icon_value)

        self._template = template

    def is_accessible(self):
        return current_user.role.name == "Administrator"

    def inaccessible_callback(self, name, **kwargs):
        flash('You are not administrator. Please change to Administrator account')
        return redirect(url_for('auth.login'))

class MyAdmin(Admin):

    def __init__(self, app=None, name=None,
                 url=None, subdomain=None,
                 index_view=None,
                 translations_path=None,
                 endpoint=None,
                 static_url_path=None,
                 base_template=None,
                 template_mode=None,
                 category_icon_classes=None):
        super(MyAdmin, self).__init__(app=app or None, name=name or 'Admin',
                                      url=url or None, subdomain=subdomain or None,
                                      index_view=index_view or None,
                                      translations_path=None,
                                      endpoint=endpoint or None,
                                      static_url_path=static_url_path or None,
                                      base_template=base_template or None,
                                      template_mode=template_mode or None,
                                      category_icon_classes=category_icon_classes or None)
        self.blueprint = None

    def _set_admin_index_view(self, index_view=None,
                              endpoint=None, url=None):
        """
            Add the admin index view.

          :param index_view:
               Home page view to use. Defaults to `AdminIndexView`.
           :param url:
               Base URL
          :param endpoint:
               Base endpoint name for index view. If you use multiple instances of the `Admin` class with
               a single Flask application, you have to set a unique endpoint name for each instance.
        """
        self.index_view = index_view or AdminIndexView(endpoint=endpoint, url=url)
        self.endpoint = endpoint or self.index_view.endpoint
        self.url = url or self.index_view.url

        # Add predefined index view
        # assume index view is always the first element of views.
        if len(self._views) > 0:
            self._views[0] = self.index_view
            self._menu[0] = MenuView(self.index_view.name, self.index_view)
        else:
            self.blueprint = self.index_view.create_blueprint(self)

# Another way use blue print class
# class AdminBlueprint(Blueprint):
#     views = None

#     def __init__(self, *args, **kwargs):
#         self.views = []
#         return super(AdminBlueprint, self).__init__('admin2', __name__, url_prefix='/admin2', static_folder='static', static_url_path='/static/admin2')  # 也可以用super()

#     def add_view(self, view):
#         self.views.append(view)

#     def register(self, app, options, first_registration=False):
#         # admin = MyAdmin(name='micrblog', template_mode='bootstrap3', index_view=MyAdminIndexView())
#         # admin.init_app(app)
#         for v in self.views:
#             admin.add_view(v)
#         return super().register(app, options)

# admin = AdminBlueprint()
# admin.add_view(ModelView(User, db.session))
# admin.add_view(ModelView(Post, db.session))
