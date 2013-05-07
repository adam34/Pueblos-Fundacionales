#archivo de templatetags llamado tags.py
from django.template import Library

register = Library()
#Es una metodo para obtener un elemento de una lista
@register.filter
def dir_python(obj):
	print type(obj)
	return dir(obj)

@register.filter
def get_value(obj):
	return obj

@register.simple_tag
def put_fns():
	script = '<script type="text/javascript" src="/static/admin/js/fns.js"></script>'
	return script