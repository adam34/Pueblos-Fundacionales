#archivo de templatetags llamado tags.py
from django.template import Library

register = Library()
#Es una metodo para obtener un elemento de una lista
@register.simple_tag
def put_fns(obj,nombre, tipo):
	#data = nombre , type_template
	print nombre
	print tipo
	try:
		js=''
		if tipo =='add':
			for jss in obj._js:
				temp = jss			
				if temp.endswith(nombre+'.js'):
					js=jss
					break
		elif tipo =='change':
			for jss in obj._js:
				temp = jss			
				if temp.endswith(nombre+'_change.js'):
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