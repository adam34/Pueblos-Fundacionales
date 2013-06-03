# Create your views here.
# -*- encoding: utf-8 -*-
	# import pdb
	# pdb.set_trace()
import json
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.models import User
from django.conf import settings

from administrador.models import *
from django.db.models import Max
from django.views.decorators.csrf import csrf_exempt
from django.utils.translation import get_language_info,ugettext as _
from django.views import i18n
from django.contrib.auth import authenticate,logout,login
from django.core.mail import send_mail
from email.MIMEText import MIMEText
import string, random,datetime,json,smtplib

def home(request): 
	# #Obtener un pueblo turistico al azar
	try:
		#Se obtienen los pueblos turisticos solamente y se elige 1 al azar.
		# import pdb
		# pdb.set_trace()
		cantidad_turisticos=pueblo.objects.filter(TIPO=u'T').count()
		turistico = None
		if cantidad_turisticos > 0:
			azar=random.randint(0,cantidad_turisticos-1)
			turistico=pueblo.objects.all()[azar]
		cantidad_curiosidades=curiosidad.objects.count()
		#Procedimiento similar al de pueblos turisticos pero con las curiosidades
		curios=None
		if cantidad_curiosidades > 0:
			azar=random.randint(0,cantidad_curiosidades-1)
			curios=curiosidad.objects.all()[azar]
		#Se obtiene el pueblo más visitado y los 4 más visitados
		total_pueblos=pueblo.objects.count()
		pueblo_masVisitado=None
		pueblos_masVisitados=None
		if total_pueblos >0:
			pueblos_masVisitados=pueblo.objects.order_by('-VISITAS')[:4]
			pueblo_masVisitado=pueblos_masVisitados[0]
		#Se obtienen los sitios con contrato vigente y con menor numero de veces desplegados
		total_contratos=contrato.objects.count()
		contracts=None
		if total_contratos>0:
			contracts=[]
			hoy=datetime.date.today()
			fechas=contrato.objects.all().order_by('NOVECES')
			for fecha in fechas:
				tiempo=datetime.timedelta(days=30*fecha.DURACION)
				fin=fecha.FECHA_INICIO+tiempo
				inicio=fecha.FECHA_INICIO
				if (inicio<=hoy and hoy<=fin):
					fecha.NOVECES+=1
					fecha.save()
					contracts.append(fecha)
				if len(contracts)>=2:
					break
			#contracts = contrato.objects.all().order_by('NOVECES')[:2]
		#Obtener los 3 primeros
		# import pdb
		# pdb.set_trace()
		hoy_time=datetime.datetime.now()
		eventos_hoy=evento.objects.filter(FECHA__day=hoy_time.day).order_by('FECHA')
		if eventos_hoy.count()<=0:
			eventos_hoy=None
		eventos_mes=evento.objects.filter(FECHA__year=hoy_time.year,FECHA__month=hoy_time.month).order_by('FECHA')
		if eventos_mes.count()<=0:
			eventos_mes=None

	except Exception,e:
		print e
	return render_to_response('index.html',RequestContext(request,{
		'user':request.user,
		'turistico':turistico,
		'curiosidad':curios,
		'mas_visto':pueblo_masVisitado,
		'mas_vistos':pueblos_masVisitados,
		'contratos':contracts,
		'eventos_hoy':eventos_hoy,
		'eventos_mes':eventos_mes,
		}))
def eventos_ajax(request):
	# import pdb
	# pdb.set_trace()
	if request.is_ajax():
		if request.POST:
			if ('year' in request.POST and 'month' in request.POST):
				year=int(request.POST['year'])
				month=int(request.POST['month'])
				eventos_mes=evento.objects.filter(FECHA__year=year,FECHA__month=month).order_by('FECHA')[:3]
				if eventos_mes.count()<=0:
					return HttpResponse(json.dumps({'respuesta':'noDatos'}),mimetype='application/json')
				else:
					respuesta=[]
					for evento_mes in eventos_mes:
						dicc = dict()
						dicc['day']=evento_mes.FECHA.day
						dicc['month']=evento_mes.FECHA.month
						dicc['year']=evento_mes.FECHA.year
						dicc['nombre']=evento_mes.NOMBRE
						dicc['id']=evento_mes.ID
						respuesta.append(dicc)
					return HttpResponse(json.dumps({'respuesta':'exito','eventos':respuesta}),mimetype='application/json')
			else:
				return HttpResponse(json.dumps({'respuesta':'noCampos'}),mimetype='application/json')
		else:
			return HttpResponse(json.dumps({'respuesta':'noPOST'}),mimetype='application/json')
	else:
		return HttpResponse(json.dumps({'respuesta':'noAJAX'}),mimetype='application/json')

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
