import functools
from werkzeug.routing import Map, Rule


class Router(object):

    url_map = Map()
    controllers = dict()

    @classmethod
    def route(cls, rule, methods=['GET'], endpoint=None, **options):
        def decorator(f):
            # @functools.wraps(f)
            # def wrapper(self, rule, methods=['GET'], endpoint=None, **options):
            class_ = f.__qualname__.split('.')
            module_ = f.__module__.split('.')
            cls.add_url_rule(rule, methods, class_[1], **options)
            cls.controllers[endpoint] = (module_[1], class_[0], class_[1]) # { 'auth': ('app.controller.AppController', 'AppController.auth')}
            return f
        return decorator
    
    @classmethod
    def add_url_rule(cls, rule, methods=['GET'], endpoint=None, **options):
        rule = Rule(rule, methods=methods, endpoint=endpoint)
        cls.url_map.add(rule)