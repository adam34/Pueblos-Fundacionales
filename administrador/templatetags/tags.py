#archivo de templatetags llamado tags.py
from django.template import Library
from django.forms.widgets import Media
from administrador.models import *
from django.utils.safestring import mark_safe
from django.utils.html import conditional_escape, format_html, format_html_join

register = Library()
#Es una metodo para obtener un elemento de una lista
# @register.simple_tag
# def put_js(nombre, tipo):
# 	nombre = nombre.encode()
# 	js = None
# 	if tipo =='add':
# 		if nombre =='users':
# 			js=('/static/admin/js/users.js','/static/admin/js/jquery.multi-select.js','/static/admin/js/jquery.quicksearch.js',)
# 		elif nombre =='grupos':
# 			js=('/static/admin/js/grupos.js','/static/admin/js/jquery.multi-select.js','/static/admin/js/jquery.quicksearch.js',)
# 		elif nombre =='pueblos':
# 			pass
# 			# js=('/static/tiny_mce/tiny_mce.js',)
# 	elif tipo == 'change':
# 		if nombre =='users':
# 			js=('/static/admin/js/users.js','/static/admin/js/jquery.multi-select.js','/static/admin/js/jquery.quicksearch.js',)
# 		elif nombre =='grupos':
# 			js=('/static/admin/js/grupos.js','/static/admin/js/jquery.multi-select.js','/static/admin/js/jquery.quicksearch.js',)
# 		elif nombre =='pueblos':
# 			pass
# 			# js=('/static/tiny_mce/tiny_mce.js',)
# 	if js is None:
# 		return
# 	else:
# 		obj = Media()
# 		obj._css={}
# 		obj._js=js
# 	return obj.render()

# @register.simple_tag
# def put_css(nombre, tipo):
# 	nombre = nombre.encode()
# 	css=None
# 	# import pdb
# 	# pdb.set_trace()
# 	if tipo =='add':
# 		if nombre =='users':
# 			css={'all':('/static/admin/css/multi-select.css',),}
# 		elif nombre =='grupos':
# 			css={'all':('/static/admin/css/multi-select.css',),}
# 	elif tipo == 'change':
# 		if nombre =='users':
# 			css={'all':('/static/admin/css/multi-select.css',),}
# 		elif nombre =='grupos':
# 			css={'all':('/static/admin/css/multi-select.css',),}
# 	if css is None:
# 		return
# 	else:

# 		obj = Media()
# 		obj._css=css
# 		obj._js=()
# 		return obj.render()

@register.simple_tag
def mostrar_relatos():
	relatos=relato.objects.filter(APROBADO=0).order_by('-FECHA')
	html = []
	for rel in relatos:
		html.append(mark_safe("""
		<tr>
				<td><a href='/admin/administrador/relato/"""+str(rel.ID)+"""/'>"""+rel.USUARIO.username+"""</a></td>
				<td>"""+rel.PUEBLO.NOMBRE+"""</td>
				<td>"""+rel.FECHA.strftime("%d/%m/%Y %H:%M:%S")+"""</td>
		</tr>
			""")
			)
	if len(html)>0:
		return mark_safe('\n'.join(html))
	else:
		return

@register.simple_tag
def mostrar_reportes():
	# import pdb
	# pdb.set_trace()
	reportes=reporte_comentario.objects.all().order_by('-FECHA')
	html = []	
	for reporte in reportes:
		tipo=""
		comentario= None
		if reporte.CLASE_COMENTARIO=='P':
			tipo='Pueblo'
			try:
				comentario=comentario_pueblo.objects.get(ID=reporte.COMENTARIO)
			except comentario_pueblo.DoesNotExist, e:
				pass
		elif reporte.CLASE_COMENTARIO=='R':
			tipo='Relato'
			try:
				comentario=comentario_relato.objects.get(ID=reporte.COMENTARIO)
			except comentario_relato.DoesNotExist, e:
				pass
		elif reporte.CLASE_COMENTARIO=='E':
			tipo='Evento'
			try:
				comentario=comentario_evento.objects.get(ID=reporte.COMENTARIO)
			except comentario_evento.DoesNotExist, e:
				pass
		elif reporte.CLASE_COMENTARIO=='S':
			tipo='Sitio'
			try:
				comentario=comentario_sitio.objects.get(ID=reporte.COMENTARIO)
			except comentario_sitio.DoesNotExist, e:
				pass
		else:
			tipo='Error'
		html.append(mark_safe("""
		<tr>
				<td><a href='/admin/administrador/reporte_comentario/"""+str(reporte.ID)+"""/'>"""+reporte.USUARIO.username+"""</a></td>
				<td>"""+tipo+"""</td>
				<td>"""+reporte.FECHA.strftime("%d/%m/%Y %H:%M:%S")+"""</td>
		</tr>
			""")
			)
	if len(html)>0:
		return mark_safe('\n'.join(html))
	else:
		return

@register.simple_tag
def mostrar_logins(user):
	# import pdb
	# pdb.set_trace()
	if user.is_superuser:
		access=login.objects.all().order_by('-FECHA')[:10]
	else:
		access=login.objects.filter(USUARIO=user).order_by('-FECHA')[:10]
	html = []
	for acc in access:
		html.append(mark_safe("""
		<tr>
				<td><a href='/admin/administrador/login/"""+str(acc.ID)+"""/'>"""+acc.USUARIO.username+"""</a></td>
				<td>"""+acc.FECHA.strftime("%d/%m/%Y %H:%M:%S")+"""</td>
		</tr>
			""")
			)
	if len(html)>0:
		return mark_safe('\n'.join(html))
	else:
		return



@register.filter
def cmp_str(var1, valor1):
	# import pdb
	# pdb.set_trace()
	valor1 = valor1.encode()
	valor2 = var1.encode()
	if valor1 == valor2:
		return True
	else:
		return False

@register.filter
def get_value(obj):
	return obj

@register.filter
def get_type(obj):
	return type(obj)

@register.filter
def dir_python(obj):
	import pdb
	pdb.set_trace()
	return dir(obj)