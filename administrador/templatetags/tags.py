#archivo de templatetags llamado tags.py
from django.template import Library

register = Library()
#Es una metodo para obtener un elemento de una lista
@register.filter
def put_fns(obj,nombre):
	try:
		js=''
		for jss in obj._js:
			temp = jss
			if temp.endswith(nombre+'.js'):
				js=jss
				break
		lista=[js]
		obj._js=lista
		return obj.render()
	except IndexError:
		return []

@register.filter
def get_value(obj):
	return obj

@register.filter
def dir_python(obj):
	print type(obj)
	print obj
	return dir(obj)