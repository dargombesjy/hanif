import sys
import pkgutil
from werkzeug.utils import import_string


class Environment(object):
    def __init__(self, path):
        self.modules = dict()
        self.controllers = dict()
        self.load_packages(path)

    
    def load_packages(self, path):   #, basename='modules'):
        if isinstance(path, str):
            paths = path.split(',')
            for path in paths:
                lpath = path.split('/')
                basename = lpath.pop()
                parent = '/'.join(lpath)
                if not parent in sys.path:
                    sys.path.append(parent)
                self.import_modules([path], basename)
    
    def import_modules(self, path, basename):
        for _importer, modname, ispkg in pkgutil.iter_modules(path):
            if ispkg:
                import_name = basename + '.' + modname
                module = import_string(import_name)
                controller = getattr(module, 'controller', False)
                if controller:
                    self.controllers[modname] = controller
                else:
                    self.modules[modname] = module
            elif modname == 'controller':
                import_name = basename + '.' + modname
                controller = import_string(import_name)
                self.controllers[modname] = controller

    def get_module(self, module_name):
        arr_ = module_name.split('.')
        if arr_[0] in self.modules:
            module = getattr(self.modules[arr_[0]], arr_[1])
            module.env = self
            return module
        return None