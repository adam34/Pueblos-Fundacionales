#archivo de templatetags llamado tags.py
from django.template import Library

register = Library()
#Es una metodo para obtener un elemento de una lista
@register.filter
def get_list(list):
	return 1

@register.simple_tag
def put_fns():
	script = '<script type="text/javascript" src="/static/admin/js/fns.js"></script>'
	return script