from jinja2 import Environment, FileSystemLoader, select_autoescape
from werkzeug import Response


class BaseController(object):
    
    def __init__(self, env) -> None:
        self.env = env
        self.templates = Environment(
            loader=FileSystemLoader(['/home/warno006089/workspace/hanif/templates']),
            autoescape=select_autoescape()
        )

    def render_html(self, template_name, context=None):
        template = self.templates.get_template(template_name)
        html = template.render(data=context)
        return Response(html, content_type='text/html')

    def json_output(self, request):
        return Response('json')