# Create your views here.
# -*- encoding: utf-8 -*-
	# import pdb
	# pdb.set_trace()
import json
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response,redirect
from django.template import RequestContext
from django.contrib.auth.models import User
from django.conf import settings

from administrador.models import *
from django.views.decorators.csrf import csrf_exempt
from django.utils.translation import get_language_info,ugettext as _
from django.views import i18n
from django.contrib.auth import authenticate,logout,login
from django.core.mail import send_mail
from email.MIMEText import MIMEText
import string, random
import json,smtplib

def home(request): 
	# import pdb
	# pdb.set_trace()
	#Obtener un pueblo turistico al azar
	# cantidad_turisticos=pueblo.objects.filter(TIPO=u'Turístico').count()
	# azar=random.randint(0,cantidad_turisticos-1)
	return render_to_response('index.html',RequestContext(request,{'user':request.user}))

def login_ajax(request):
	# import pdb
	# pdb.set_trace()
	if request.is_ajax():
		if request.POST:
			if not request.user.is_authenticated():
				if (request.POST.__contains__('usuario') and request.POST.__contains__('password')):
					username = request.POST['usuario']
					password = request.POST['password']
					if username and password:
						usuario = authenticate(username=username,
														password=password)
						if usuario is not None:
							if not usuario.is_active:
								return HttpResponse(json.dumps({'respuesta':'noActivo'}),mimetype='application/json')
							else:
								login(request,usuario)
								return HttpResponse(json.dumps({'respuesta':'exito'}),mimetype='application/json')
						else:
								return HttpResponse(json.dumps({'respuesta':'fallido'}),mimetype='application/json')
				else:
					return HttpResponse(json.dumps({'respuesta':'noCampos'}),mimetype='application/json')
			else:
				return HttpResponse(json.dumps({'respuesta':'noAccion'}),mimetype='application/json')
		else:
			return HttpResponse(json.dumps({'respuesta':'noPOST'}),mimetype='application/json')
	else:
		return HttpResponse(json.dumps({'respuesta':'noAJAX'}),mimetype='application/json')
	pass

def registro_usuario_ajax(request):
	if request.is_ajax():
		if request.POST:
			if ('usuario' in request.POST and 'correo' in request.POST and 'password' in request.POST and 'password_repe' in request.POST):
				usuario = request.POST['usuario']
				password = request.POST['password']
				password_repe =request.POST['password_repe']
				if password == password_repe:
					if not User.objects.filter(username=usuario).exists():
						nuevo_usuario=User(username=usuario)
						nuevo_usuario.set_password(password)
						nuevo_usuario.email=request.POST['correo']
						nuevo_usuario.save()
						try:
							# msg = MIMEText(message, _charset="UTF-8")
							# msg['Subject'] = Header(subject, "utf-8")
							server = smtplib.SMTP('smtp.gmail.com', 587) 
							#Next, log in to the server
							server.starttls()
							server.ehlo()
							server.login("mario250213", "/(mar3443)=")
							mensaje = u"Bienvenido %s, al sistema de Pueblos Fundacionales! Esperamos que tenga una buena experiencia. \n\n\n Atentamente: La administración del sistema de Pueblos Fundacionales" % (usuario)
							msg = MIMEText(mensaje,_charset="UTF-8")
							msg['From'] = "mario250213@gmail.com"
							msg['To'] = nuevo_usuario.email
							msg['Subject'] = "Registro de cuenta en sitio de Pueblos Fundacionales."							
							text = msg.as_string()
							server.sendmail("mario250213@gmail.com", nuevo_usuario.email, text)
							server.quit()
							print "enviado"
						except  Exception,e:
							print e
						return HttpResponse(json.dumps({'respuesta':'exito'}),mimetype='application/json')
					else:
						return HttpResponse(json.dumps({'respuesta':'existe'}),mimetype='application/json')
				else:
					return HttpResponse(json.dumps({'respuesta':'noIguales'}),mimetype='application/json')
			else:
				return HttpResponse(json.dumps({'respuesta':'noCampos'}),mimetype='application/json')
		else:
			return HttpResponse(json.dumps({'respuesta':'noPOST'}),mimetype='application/json')	
	else:
		return HttpResponse(json.dumps({'respuesta':'noAJAX'}),mimetype='application/json')

def recupera_ajax(request):
	if request.is_ajax():
		if request.POST:
			if 'correo' in request.POST :
				correo = request.POST['correo']
				usuario = User.objects.filter(email=correo)
				if usuario.exists():
					try:
						# import pdb
						# pdb.set_trace()
						# msg = MIMEText(message, _charset="UTF-8")
						# msg['Subject'] = Header(subject, "utf-8")
						server = smtplib.SMTP('smtp.gmail.com', 587) 
						#Next, log in to the server
						server.starttls()
						server.ehlo()
						nueva_contrasena = ''.join(random.choice(string.ascii_uppercase+string.ascii_lowercase + string.digits) for x in range(15))
						usuario[0].set_password(nueva_contrasena)
						usuario[0].save()
						server.login("mario250213", "/(mar3443)=")
						mensaje = u"Qué tal %s.<br>La contraseña de recuperación de su cuenta es: %s\n<br> Para cambiar la contraseña actual por una personal, haga clic sobre el enlace siguiente: <a href='http://localhost/cambiar_contraseña/'>http://localhost/cambiar_contraseña/</a>  <br><br> Atentamente: La administración del sistema de Pueblos Fundacionales" % (usuario[0].username,nueva_contrasena)
						msg = MIMEText(mensaje,'html',_charset="UTF-8")
						msg['From'] = "mario250213@gmail.com"
						msg['To'] = correo
						msg['Subject'] = u"Recuperar contraseña."
						text = msg.as_string()
						server.sendmail("mario250213@gmail.com", correo, text)
						server.quit()
						print "enviado"
					except  Exception,e:
						print e
					return HttpResponse(json.dumps({'respuesta':'exito'}),mimetype='application/json')
				else:
					return HttpResponse(json.dumps({'respuesta':'Noexiste'}),mimetype='application/json')
			else:
				return HttpResponse(json.dumps({'respuesta':'noCampos'}),mimetype='application/json')
		else:
			return HttpResponse(json.dumps({'respuesta':'noPOST'}),mimetype='application/json')	
	else:
		return HttpResponse(json.dumps({'respuesta':'noAJAX'}),mimetype='application/json')

def cambiar_contrasena(request):
	if request.POST:
		if ('usuario' in request.POST and 'contrasena' in request.POST and 'contrasena_repe' in request.POST):
			contrasena= request.POST['contrasena']
			contrasena_repe=request.POST['contrasena_repe']
			if contrasena == contrasena_repe:
				usuario = request.POST['usuario']
				usuario_actual = User.objects.get(username=usuario)
				usuario_actual.set_password(contrasena)
				return HttpResponse(json.dumps({'respuesta':'exito'}),mimetype='application/json')
			else:
				return HttpResponse(json.dumps({'respuesta':'noIguales'}),mimetype='application/json')
		else:
			return HttpResponse(json.dumps({'respuesta':'noCampos'}),mimetype='application/json')
	elif request.GET:
		if 'correo' in request.GET:
			try:
				correo=request.GET['correo']
				usuario_actual = User.objects.get(email=correo)
				return render_to_response('cambiar_contrasena.html',RequestContext(request,{'user':usuario_actual}))
			except Exception,e:
				print e
				raise Http404
		else:
			raise Http404
	else:
		raise Http404

def cerrar_sesion(request):
	logout(request)
	return redirect(home)




def secciones(request): 
	return render_to_response('secciones.html')

def pueblos(request): 
	return render_to_response('pueblos.html')

def politicas(request): 
	return render_to_response('politicas.html')

def curiosidades(request): 
	return render_to_response('curiosidades.html')

def masvisto(request): 
	return render_to_response('mas-visto.html')

def descubrabcs(request): 
	return render_to_response('descubra-bcs.html')

def bcsdesconocida(request): 
	return render_to_response('bcs-desconocida.html')

def galerias(request):
	objs=galeria.objects.all()
	return render_to_response('galerias.html',RequestContext(request,{'galerias':objs}))

def galerias_ajax(request):
	# import pdb
	# pdb.set_trace()
	if request.is_ajax():
		if request.POST:
			if request.POST.__contains__('galeria'):
				nombre = request.POST['galeria']
				galer=galeria.objects.filter(NOMBRE=nombre)[0]
				archivos = galer.ARCHIVOS.all()
				dicc = {}
				dicc['archivos'] =[]
				for arc in archivos:
					dicc['archivos'].append(arc.RUTA.url)
				return HttpResponse(json.dumps(dicc),mimetype='application/json')
			else:
				return HttpResponse(json.dumps({'archivos':None}),mimetype='application/json')
		else:
			return HttpResponse(json.dumps({'archivos':None}),mimetype='application/json')
	else:
		raise Http404

def libros(request): 
	return render_to_response('libros.html')

def basico(request): 
	return render_to_response('accesos.html')

def mapa(request): 
	return render_to_response('mapa.html')

def alojamiento(request): 
	return render_to_response('alojamiento.html')

def comida(request): 
	return render_to_response('comida.html')

def info(request): 
	return render_to_response('info-pueblos.html')

def dir(request): 
	return render_to_response('directorio.html')

def humans(request): 
	return render_to_response('humans.txt')

def libreria(request): 
	return render_to_response('libreria.html')

def p(request): 
	return render_to_response('pueblos/purisima.html')

def l(request): 
	return render_to_response('pueblos/loreto.html')

def libro_p(request): 
	return render_to_response('libreria/libro_purisima.html')

def multimedia(request):
	return render_to_response('multimedia.html')

def player(request):
	return render_to_response('multimedia/player.html')

def audio(request):
	return render_to_response('multimedia/audio.html')

def eventos(request):
	eventos=evento.objects.all()
	return render_to_response('eventos.html',{'eventos':eventos})

def galeria_2(request):
	return render_to_response('multimedia/galeria.html')

def relatos(request):
	relatos = relato.objects.all()
	return render_to_response('relatos.html',{'relatos':relatos})

def sitiosT(request):
	sitios = sitio_turistico.objects.all()
	return render_to_response('sitios_turisticos.html',{'sitios':sitios})

def busqueda(request):
	return render_to_response('busqueda.html')
