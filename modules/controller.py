from app.controller import BaseController
from app.router import Router
from werkzeug import Response


class Controller(BaseController):
    
    @Router.route('/', ['GET'], 'home')
    def home(self, request):
        return self.render_html('home.html', {'test': 'lulus'})

    @Router.route('/auth', ['GET', 'POST'], 'auth')
    def auth(self, request):
        return Response('Auth')

    @Router.route('/account', ['GET', 'POST'], 'account')
    def account(self, request):
        obj_c = self.env.get_module('accounting.AccountMove')
        obj_form = obj_c.create_form()
        form = obj_form(request.form)
        if request.method == 'POST':
            obj = obj_c()
            obj.create(**form.data)
        return self.render_html('accounting/account.html', form)
        
