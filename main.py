import os
import logging
from app.env import Environment
from app.http import Application
from app.router import Router
from werkzeug.middleware.shared_data import SharedDataMiddleware


def create_app():
    Env = Environment('/home/warno006089/workspace/hanif/modules')
    App = Application(Env, Router)
    # logging.basicConfig()
    # logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
    return App

if __name__ == '__main__':
    from werkzeug.serving import run_simple
    app_ = create_app()
    exports = {
        '/static': os.path.join(os.path.dirname(__file__), 'static'),
    }
    app = SharedDataMiddleware(app_, exports)
    run_simple('127.0.0.1', 5000, app, use_debugger=True, use_reloader=False)
