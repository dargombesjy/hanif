from app.controller import BaseController
from app.router import Router
from werkzeug import Response


class AdminController(BaseController):

    @Router.route('/admin', ['GET', 'POST'], 'admin')
    def admin(self, request):
        return self.render_html('admin/admin.html', {'name': 'admin'})