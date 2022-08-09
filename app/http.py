# import functools
from werkzeug.utils import import_string
from werkzeug.wrappers import Request
# from werkzeug.routing import Map, Rule
from werkzeug.exceptions import HTTPException


class Application(object):

    def __init__(self, env, router):   # , config):
        self.env = env
        self.url_map = router.url_map   # Map()
        self.controllers = router.controllers  # dict()

    def wsgi_app(self, environ, start_response):
        request = Request(environ)
            # test
            # sid = request.cookies.get('session_id')
            # if sid is None:
            #     request.session = session_store.new()
            # else:
            #     request.session = session_store.get(sid)
            # message = self.env['message']
            # message.message = []
            # message.user = request.session.get('user')
            # end test
        response = self.dispatch_request(request)
            # test
            # if request.session and request.session.should_save:
            #     session_store.save(request.session)
            #     response.set_cookie('session_id', request.session.sid)
            # end test
        return response(environ, start_response)

    def dispatch_request(self, request):
        adapter = self.url_map.bind_to_environ(request.environ)
        try:
            endpoint, url_params = adapter.match()
            request.url_params = url_params
            module_, classname_, methodname_ = self.controllers[endpoint]
            cls_ = getattr(self.env.controllers[module_], classname_)
            controller = cls_(self.env)
            method_ = getattr(controller, methodname_)
            response = method_(request)
        except HTTPException as e:
            return e
        return response

    def reverse_url(self, endpoint, **params):
        urls = self.url_map.bind('localhost')
        return urls.build(endpoint, **params)
        
    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)

