#archivo de templatetags llamado tags.py
from django.template import Library
from django.forms.widgets import Media

register = Library()
#Es una metodo para obtener un elemento de una lista
@register.simple_tag
def put_js(nombre, tipo):
	# js=''
	# if tipo =='add':
	# 	for jss in obj._js:
	# 		temp = jss			
	# 		if temp.endswith(nombre+'.js'):
	# 			js=jss
	# 			break
	# elif tipo =='change':
	# 	for jss in obj._js:
	# 		temp = jss			
	# 		if temp.endswith(nombre+'_change.js'):
	# 			js=jss
	# 			break
	# lista=[js]
	# obj._js=lista
	# import pdb
	# pdb.set_trace()
	nombre = nombre.encode()
	js = None
	if tipo =='add':
		if nombre =='users':
			js=('/static/admin/js/users.js','/static/admin/js/jquery.multi-select.js','/static/admin/js/jquery.quicksearch.js',)
		elif nombre =='grupos':
			js=('/static/admin/js/grupos.js','/static/admin/js/jquery.multi-select.js','/static/admin/js/jquery.quicksearch.js',)
	elif tipo == 'change':
		if nombre =='users':
			js=('/static/admin/js/users.js','/static/admin/js/jquery.multi-select.js','/static/admin/js/jquery.quicksearch.js',)
		elif nombre =='grupos':
			js=('/static/admin/js/grupos.js','/static/admin/js/jquery.multi-select.js','/static/admin/js/jquery.quicksearch.js',)
	if js is None:
		return ()
	else:
		obj = Media()
		obj._css={}
		obj._js=js
	return obj.render()

@register.simple_tag
def put_css(nombre, tipo):
	nombre = nombre.encode()
	css=None
	# import pdb
	# pdb.set_trace()
	if tipo =='add':
		if nombre =='users':
			css={'all':('/static/admin/css/multi-select.css',),}
		elif nombre =='grupos':
			css={'all':('/static/admin/css/multi-select.css',),}
	elif tipo == 'change':
		if nombre =='users':
			css={'all':('/static/admin/css/multi-select.css',),}
		elif nombre =='grupos':
			css={'all':('/static/admin/css/multi-select.css',),}
	if css is None:
		return ()
	else:

		obj = Media()
		obj._css=css
		obj._js=()
		return obj.render()

@register.filter
def get_value(obj):
	return obj

@register.filter
def get_type(obj):
	return type(obj)

@register.filter
def dir_python(obj):
	#print type(obj)
	#print obj
	return dir(obj)