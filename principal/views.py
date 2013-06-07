# Create your views here.
# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
	# import pdb
	# pdb.set_trace()
import json
from django.http import HttpResponse, Http404,HttpResponseRedirect
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models import Q

from administrador.models import *
from django.db.models import Max
from django.views.decorators.csrf import csrf_exempt
from django.utils.translation import get_language_info,ugettext as _
from django.utils import translation
from django.views import i18n
from django.contrib.auth import authenticate,logout,login
from django.core.mail import send_mail
from email.MIMEText import MIMEText
import string, random,datetime,json,smtplib

def home(request): 	
	# #Obtener un pueblo turistico al azar
	# import pdb
	# pdb.set_trace()
	url=resolver_url(request)
	language=obtener_idioma(request)
	try:
		#Se obtienen los pueblos turisticos solamente y se elige 1 al azar.
		cantidad_turisticos=pueblo.objects.filter(TIPO='T').count()
		turistico = None
		if cantidad_turisticos > 0:
			azar=random.randint(0,cantidad_turisticos-1)
			turistico=pueblo.objects.filter(TIPO='T')[azar]
			turistico=turistico.get_pueblo_idioma(language)
		
		#Procedimiento similar al de pueblos turisticos pero con las curiosidades
		cantidad_curiosidades=curiosidad.objects.count()
		curios=None
		if cantidad_curiosidades > 0:
			azar=random.randint(0,cantidad_curiosidades-1)
			curios=curiosidad.objects.all()[azar]
			curios=curios.get_curiosidad_idioma(language)
		#Se obtiene el pueblo más visitado y los 4 más visitados
		total_pueblos=pueblo.objects.count()
		pueblo_masVisitado=None
		pueblos_masVisitados=None
		if total_pueblos >0:
			pueblos_masVisitados=pueblo.objects.order_by('-VISITAS')[:4]
			pueblo_masVisitado=pueblos_masVisitados[0]
			pueblo_masVisitado=pueblo_masVisitado.get_pueblo_idioma(language)
		
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
		if eventos_hoy.count()>0:
			temp = []
			for even in eventos_hoy:
				temp.append(even.get_evento_idioma(language))
			eventos_hoy=temp
		else:
			eventos_hoy=None

		eventos_mes=evento.objects.filter(FECHA__year=hoy_time.year,FECHA__month=hoy_time.month).order_by('FECHA')
		if eventos_mes.count()>0:
			temp = []
			for even in eventos_mes:
				temp.append(even.get_evento_idioma(language))
			eventos_mes=temp
		else:
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
		'url':url
		}))

def eventos_ajax(request):
	# import pdb
	# pdb.set_trace()
	if request.is_ajax():
		if request.POST:
			if ('year' in request.POST and 'month' in request.POST and 'day' in request.POST):
				year=int(request.POST['year'])
				month=int(request.POST['month'])
				day=int(request.POST['day'])
				eventos_mes=evento.objects.filter(FECHA__year=year,FECHA__month=month,FECHA__day=day).order_by('FECHA')[:3]
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
						dicc['url']=u'/'+request.LANGUAGE_CODE+'/eventos/?evento='+str(evento_mes.ID)
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

#No olvidar traducir el contenido del correo
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

#No olvidar traducir el contenido del correo.
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

#Ajax
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
	# import pdb
	# pdb.set_trace()
	language=obtener_idioma(request)
	url=resolver_url(request)
	cant_elementos = sitio_turistico.objects.count()
	sitios = None
	lista = []
	try:
		if cant_elementos > 0:
			sitios = list(sitio_turistico.objects.all())
			if cant_elementos < 4:
				loop= cant_elementos
			else:
				loop=4
			for i in range(0,loop):
				azar=random.randint(0,cant_elementos-1)
				sitio = sitios[azar].get_sitio_turistico_idioma(language)
				lista.append(sitio)
				sitios.remove(sitios[azar])
				cant_elementos -=1
	except Exception, e:
		print e
		sitios=None
	return render_to_response('secciones.html',RequestContext(request,
		{
		'user':request.user,
		'sitios':lista,
		'url':url,
		}))

def pueblos(request):
	language=obtener_idioma(request)
	url=resolver_url(request)
	try:
		cant_pueblos= pueblo.objects.count()
		pueblos = None
		if cant_pueblos >0:
			pueblos= pueblo.objects.all()
			temp = []
			for village in pueblos:
				temp.append(village.get_pueblo_idioma(language))
			pueblos=temp
	except Exception,e:
		print e
	return render_to_response('pueblos.html',RequestContext(request,{
		'user':request.user,
		'pueblos':pueblos,
		'url':url,
		}))

def pueblos_ajax(request):
	# import pdb
	# pdb.set_trace()
	language=obtener_idioma(request)
	if request.is_ajax():
		if request.POST:
			if 'NOMBRE' in request.POST:
				try:				
					nombre = request.POST['NOMBRE']
					poblado = pueblo.objects.get(NOMBRE=nombre)
					poblado.VISITAS+=1
					poblado.save()
					temp = poblado.get_pueblo_idioma(language)
					dicc = {'NOMBRE':poblado.NOMBRE,'HISTORIA':temp.HISTORIA,'CULTURA':temp.CULTURA,'COMIDA':temp.COMIDA,'DATOS':temp.DATOS}
					return HttpResponse(json.dumps({'respuesta':'exito','pueblo':dicc}),mimetype='application/json')
				except Exception,e:
					return HttpResponse(json.dumps({'respuesta':'fallido'}),mimetype='application/json')
				else:
					return HttpResponse(json.dumps({'respuesta':'Noexiste'}),mimetype='application/json')
			else:
				return HttpResponse(json.dumps({'respuesta':'noCampos'}),mimetype='application/json')
		else:
			return HttpResponse(json.dumps({'respuesta':'noPOST'}),mimetype='application/json')	
	else:
		return HttpResponse(json.dumps({'respuesta':'noAJAX'}),mimetype='application/json')


def politicas(request):
	url=resolver_url(request)
	return render_to_response('politicas.html',RequestContext(request,
		{
		'user':request.user,
		'url':url,
		}))

def curiosidades(request):
	language=obtener_idioma(request)
	url=resolver_url(request)
	try:
		cant_curiosidades= curiosidad.objects.count()
		curiosidades = None
		if cant_curiosidades >0:
			curiosidades= curiosidad.objects.all()
			temp = []
			for curio in curiosidades:
				temp.append(curio.get_curiosidad_idioma(language))
			curiosidades=temp
	except Exception,e:
		print e
	return render_to_response('curiosidades.html',RequestContext(request,
		{
		'user':request.user,
		'curiosidades':curiosidades,
		'url':url,
		}))

def masvisto(request):
	# import pdb
	# pdb.set_trace()
	language=obtener_idioma(request)
	url=resolver_url(request)
	try:
		cant_pueblos= pueblo.objects.count()
		mas_visto = None
		if cant_pueblos >0:
			mas_visto= pueblo.objects.all().order_by('-VISITAS')[0]
			temp=mas_visto.get_pueblo_idioma(language)
			mas_visto=temp
	except Exception,e:
		print e
	return render_to_response('mas-visto.html',RequestContext(request,
		{
		'user':request.user,
		'mas_visto':mas_visto,
		'url':url,
		}))

def descubrabcs(request):
	language=obtener_idioma(request)
	url=resolver_url(request)
	try:
		cant_turisticos= pueblo.objects.filter(TIPO='T').count()
		turisticos = None
		if cant_turisticos >0:
			turisticos= pueblo.objects.filter(TIPO='T')
			temp=[]
			for turistico in turisticos:
				temp.append(turistico.get_pueblo_idioma(language))
			turisticos=temp
	except Exception,e:
		print e
	return render_to_response('descubra-bcs.html',RequestContext(request,
		{
		'user':request.user,
		'turisticos':turisticos,
		'url':url,
		}))

def bcsdesconocida(request):
	language=obtener_idioma(request)
	url=resolver_url(request)
	try:
		cant_curiosidades= curiosidad.objects.count()
		curiosidades = None
		if cant_curiosidades >0:
			curiosidades= curiosidad.objects.all()
			temp=[]
			for curio in curiosidades:
				temp.append(curio.get_curiosidad_idioma(language))
			curiosidades=temp
	except Exception,e:
		print e
	return render_to_response('bcs-desconocida.html',RequestContext(request,
		{
		'user':request.user,
		'curiosidades':curiosidades,
		'url':url,
		}))

def galerias(request):
	url=resolver_url(request)
	objs=galeria.objects.all()
	return render_to_response('galerias.html',RequestContext(request,
		{
		'galerias':objs,
		'user':request.user,
		'url':url,
		}))

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
	language=obtener_idioma(request)
	url=resolver_url(request)
	hoy = datetime.datetime.now()
	cont_eventos = evento.objects.filter(FECHA__gt=hoy)
	eventos = None
	if cont_eventos > 0:
		eventos = evento.objects.filter(FECHA__gt=hoy)
		temp = []
		for event in eventos:
			temp.append(event.get_evento_idioma(language))
		eventos=temp
	return render_to_response('libros.html',RequestContext(request,
		{
		'user':request.user,
		'eventos':eventos,
		'url':url,
		}))

def basico(request):
	url=resolver_url(request)
	return render_to_response('accesos.html',RequestContext(request,
		{
		'user':request.user,
		'url':url,
		}))

#Ver si es necesario traducir la información en este.
def mapa(request):
	language=obtener_idioma(request)
	url=resolver_url(request)
	try:
		cant_fund= pueblo.objects.filter(TIPO='F').count()
		pueblos_fund = None
		if cant_fund >0:
			pueblos_fund= pueblo.objects.filter(TIPO='F')
			temp = []
			for pueb in pueblos_fund:
				temp.append(pueb.get_pueblo_idioma(language))
			pueblos_fund=temp
		cant_turis= pueblo.objects.filter(TIPO='T').count()
		pueblos_turis = None
		if cant_turis >0:
			pueblos_turis= pueblo.objects.filter(TIPO='T')
			temp = []
			for pueb in pueblos_turis:
				temp.append(pueb.get_pueblo_idioma(language))
			pueblos_turis=temp

		cant_sitios=sitio_turistico.objects.all()
		sitios = None
		if cant_sitios >0:
			sitios=sitio_turistico.objects.all()
			temp = []
			for site in sitios:
				temp.append(site.get_sitio_turistico_idioma(language))
			pueblos_turis=temp
	except Exception,e:
		print e
	return render_to_response('mapa.html',RequestContext(request,
		{
		'user':request.user,
		'fundacionales':pueblos_fund,
		'turisticos':pueblos_turis,
		'sitios':sitios,
		'url':url,
		}))

def alojamiento(request):
	language=obtener_idioma(request)
	url=resolver_url(request)
	try:
		try:
			categ = categoria.objects.get(NOMBRE='Hoteles')
		except Exception,e:
			categ=None
		if categ is not None:
			if sitio_turistico.objects.filter(CATEGORIA=categ).count() > 0:
				hoteles= sitio_turistico.objects.filter(CATEGORIA=categ)
				temp = []
				for hotel in hoteles:
					temp.append(hoteles.get_sitio_turistico_idioma(language))
				hoteles=temp
			else:
				hoteles=None
		else:
			hoteles=None
	except Exception,e:
		print e
	return render_to_response('alojamiento.html',RequestContext(request,
		{
		'user':request.user,
		'hoteles':hoteles,
		'url':url,
		}))

def comida(request):
	url=resolver_url(request)
	return render_to_response('comida.html',RequestContext(request,
		{
		'user':request.user,
		'url':url,
		}))

def info(request):
	url=resolver_url(request)
	return render_to_response('info-pueblos.html',RequestContext(request,
		{
		'user':request.user,
		'url':url,
		}))

def dir(request):
	url=resolver_url(request)
	return render_to_response('directorio.html',RequestContext(request,
		{
		'user':request.user,
		'url':url,
		}))

def humans(request):
	url=resolver_url(request)
	return render_to_response('humans.txt',RequestContext(request,
		{
		'user':request.user,
		'url':url,
		}))

def libreria(request):
	url=resolver_url(request)
	return render_to_response('libreria.html',RequestContext(request,
		{
		'user':request.user,
		'url':url,
		}))

def p(request):
	url=resolver_url(request)
	return render_to_response('pueblos/purisima.html',RequestContext(request,
		{
		'user':request.user,
		'url':url,
		}))

def l(request):
	url=resolver_url(request)
	return render_to_response('pueblos/loreto.html',RequestContext(request,
		{
		'user':request.user,
		'url':url,
		}))

#ajax
def libro_p(request):
	url=resolver_url(request)
	return render_to_response('libreria/libro_purisima.html',RequestContext(request,{'user':request.user}))

def multimedia(request):
	url=resolver_url(request)
	return render_to_response('multimedia.html',RequestContext(request,
		{
		'user':request.user,
		'url':url,
		}))

def multimedia_ajax(request):
	if request.is_ajax():
		if request.POST:
			if 'TIPO' in request.POST:
				tipo=request.POST['TIPO']
				if tipo =='audio':
					#buscar por .mp3
					try:
						archivos=archivo.objects.filter(RUTA__endswith='.mp3')
						if audio.count()>0:
							lista = []
							for audio in archivos:
								dicc=dict()
								dicc['NOMBRE']=audio.NOMBRE
								dicc['RUTA']=audio.RUTA
								lista.append(dicc)
							return HttpResponse(json.dumps({'respuesta':'exito','datos':lista}),mimetype='application/json')
						else:
							return HttpResponse(json.dumps({'respuesta':'noDatos'}),mimetype='application/json')
					except Exception,e:
						print e
				elif tipo == 'video':
					#buscar por .mp4,.avi
					try:
						archivos=archivo.objects.filter(RUTA__endswith=('.mp4','.avi'))
						if audio.count()>0:
							lista = []
							for audio in archivos:
								dicc=dict()
								dicc['NOMBRE']=audio.NOMBRE
								dicc['RUTA']=audio.RUTA
								lista.append(dicc)
							return HttpResponse(json.dumps({'respuesta':'exito','datos':lista}),mimetype='application/json')
						else:
							return HttpResponse(json.dumps({'respuesta':'noDatos'}),mimetype='application/json')
					except Exception,e:
						print e
				else:
					return HttpResponse(json.dumps({'respuesta':'noOpcion'}),mimetype='application/json')					
			else:
				return HttpResponse(json.dumps({'respuesta':'noCampos'}),mimetype='application/json')
		else:
			return HttpResponse(json.dumps({'respuesta':'noPOST'}),mimetype='application/json')
	else:
		return HttpResponse(json.dumps({'respuesta':'noAJAX'}),mimetype='application/json')

#Ajax
def player(request):
	return render_to_response('multimedia/player.html',RequestContext(request,{'user':request.user}))
#Ajax
def audio(request):
	return render_to_response('multimedia/audio.html',RequestContext(request,{'user':request.user}))

def eventos(request):
	language=obtener_idioma(request)
	url=resolver_url(request)
	try:
		# import pdb
		# pdb.set_trace()
		cont_eventos = evento.objects.count()
		eventos = None
		lista=[]
		if cont_eventos > 0:
			eventos = evento.objects.all()
			for event in eventos:
				dic = dict()
				coment_cont=comentario_evento.objects.filter(EVENTO=event).count()
				if coment_cont > 0:
					dic['comentarios']=comentario_evento.objects.filter(EVENTO=event)
				else:
					dic['comentarios']=[]
				
				event=event.get_evento_idioma(language)
				dic['evento']=event
				lista.append(dic)
		#Agarrar 3 comentarios por cada relato a mostrar
	except Exception,e:
		print e
	return render_to_response('eventos.html',RequestContext(request,
		{
		'user':request.user,
		'eventos':lista,
		'url':url,
		}))

def comentarios_eventos_ajax(request):
	# import pdb
	# pdb.set_trace()
	if request.is_ajax():
		if request.POST:
			if ('ID' in request.POST and 'COMENTARIO' in request.POST ):
				iden=request.POST['ID']
				comentario=request.POST['COMENTARIO']
				usuario=request.user
				try:
					event=evento.objects.get(ID=iden)
					fecha = datetime.datetime.now()
					comen_event=comentario_evento(EVENTO=event,USUARIO=usuario,DESCRIPCION=comentario,FECHA=fecha,VALORACION=0)
					comen_event.save()
					fec = fecha.strftime('%d/%m/%Y, a las %H:%M:%S ')
					return HttpResponse(json.dumps({'respuesta':'exito','fecha':fec}),mimetype='application/json')
				except Exception,e:
					print e
					return HttpResponse(json.dumps({'respuesta':'noEvento'}),mimetype='application/json')		
			else:
				return HttpResponse(json.dumps({'respuesta':'noCampos'}),mimetype='application/json')
		else:
			return HttpResponse(json.dumps({'respuesta':'noPOST'}),mimetype='application/json')
	else:
		return HttpResponse(json.dumps({'respuesta':'noAJAX'}),mimetype='application/json')


#ajax
def galeria_2(request):
	return render_to_response('multimedia/galeria.html',RequestContext(request,{'user':request.user}))


def relatos(request):
	# import pdb
	# pdb.set_trace()
	language=obtener_idioma(request)
	url=resolver_url(request)
	try:
		cont_relatos = relato.objects.count()
		relatos = None
		mejores_relatos = None
		lista=[]
		if cont_relatos > 0:
			relatos = relato.objects.filter(APROBADO=1)
			for rel in relatos:
				dic = dict()
				coment_cont=comentario_relato.objects.filter(RELATOS=rel)
				
				if coment_cont > 0:
					dic['comentarios']=comentario_relato.objects.filter(RELATOS=rel)
				else:
					dic['comentarios']=None
				rel=rel.get_relato_idioma(language)
				dic['relato']=rel
				lista.append(dic)
			mejores_relatos=relato.objects.all().order_by('-VALORACION')[:3]
		cont_pueblos= pueblo.objects.count()
		pueblos = None
		if cont_pueblos:
			pueblos = pueblo.objects.all()
		#Agarrar 3 comentarios por cada relato a mostrar
	except Exception,e:
		print e
	return render_to_response('relatos.html',RequestContext(request,
		{'relatos':lista,
		'mejores':mejores_relatos,
		'user':request.user,
		'pueblos':pueblos,
		'url':url,
		}))

def comentarios_relatos_ajax(request):
	# import pdb
	# pdb.set_trace()
	if request.is_ajax():
		if request.POST:
			if ('ID' in request.POST and 'COMENTARIO' in request.POST ):
				iden=request.POST['ID']
				comentario=request.POST['COMENTARIO']
				usuario=request.user
				try:
					rel=relato.objects.get(ID=iden)						
					fecha = datetime.datetime.now()
					comen_relato=comentario_relato(RELATOS=rel,USUARIO=usuario,DESCRIPCION=comentario,FECHA=fecha,VALORACION=0)
					comen_relato.save()
					fec = fecha.strftime('%d/%m/%Y, a las %H:%M:%S ')
					return HttpResponse(json.dumps({'respuesta':'exito','fecha':fec}),mimetype='application/json')
				except Exception,e:
					print e
					return HttpResponse(json.dumps({'respuesta':'noRelato'}),mimetype='application/json')		
			else:
				return HttpResponse(json.dumps({'respuesta':'noCampos'}),mimetype='application/json')
		else:
			return HttpResponse(json.dumps({'respuesta':'noPOST'}),mimetype='application/json')
	else:
		return HttpResponse(json.dumps({'respuesta':'noAJAX'}),mimetype='application/json')

def valorar_relatos_ajax(request):
	# import pdb
	# pdb.set_trace()
	if request.is_ajax():
		if request.POST:
			if ('ID' in request.POST and 'VALORACION' in request.POST ):
				iden=request.POST['ID']
				valoracion=int(request.POST['VALORACION'])
				usuario=request.user
				try:
					rel=relato.objects.get(ID=iden)
					vot_usuario=votacion.objects.filter(USUARIO=usuario,VOTADO=rel.ID,TIPO_COMENTARIO='r')
					if(len(vot_usuario)==0):
						valor=0
						if valoracion == 1:
							valor=1
						elif valoracion ==-1:
							valor=-1
						else:
							valor=0
						fecha = datetime.datetime.now()
						voto=votacion(VOTADO=rel.ID,USUARIO=usuario,VOTACION=valor,TIPO_COMENTARIO='r')
						voto.save()
						rel.VALORACION+=valor
						rel.save()
						return HttpResponse(json.dumps({'respuesta':'exito','valoracion':rel.VALORACION}),mimetype='application/json')
					else:
						return HttpResponse(json.dumps({'respuesta':'noVotar','valoracion':rel.VALORACION}),mimetype='application/json')
				except Exception,e:
					print e
					return HttpResponse(json.dumps({'respuesta':'noRelato'}),mimetype='application/json')
			else:
				return HttpResponse(json.dumps({'respuesta':'noCampos'}),mimetype='application/json')
		else:
			return HttpResponse(json.dumps({'respuesta':'noPOST'}),mimetype='application/json')
	else:
		return HttpResponse(json.dumps({'respuesta':'noAJAX'}),mimetype='application/json')	

def sitiosT(request):
	url=resolver_url(request)
	language=obtener_idioma(request)
	try:
		# import pdb
		# pdb.set_trace()
		cont_sitios = sitio_turistico.objects.count()
		sitios = None
		lista=[]
		if cont_sitios > 0:
			sitios = sitio_turistico.objects.all()
			for sitio in sitios:
				dic = dict()
				coment_cont=comentario_sitio.objects.filter(SITIOS=sitio).count()
				
				if coment_cont > 0:
					dic['comentarios']=comentario_sitio.objects.filter(SITIOS=sitio)
				else:
					dic['comentarios']=[]
				sitio=sitio.get_sitio_turistico_idioma(language)
				dic['sitio']=sitio
				lista.append(dic)
		#Agarrar 3 comentarios por cada relato a mostrar
	except Exception,e:
		print e
	return render_to_response('sitios_turisticos.html',RequestContext(request,
		{
		'sitios':sitios,
		'user':request.user,
		'sitios':lista,
		'url':url,
		}))

def comentarios_sitios_ajax(request):
	# import pdb
	# pdb.set_trace()
	if request.is_ajax():
		if request.POST:
			if ('ID' in request.POST and 'COMENTARIO' in request.POST ):
				iden=request.POST['ID']
				comentario=request.POST['COMENTARIO']
				usuario=request.user
				try:
					sitio=sitio_turistico.objects.get(ID=iden)						
					fecha = datetime.datetime.now()
					comen_sitio=comentario_sitio(SITIOS=sitio,USUARIO=usuario,DESCRIPCION=comentario,FECHA=fecha,VALORACION=0)
					comen_sitio.save()
					fec = fecha.strftime('%d/%m/%Y, a las %H:%M:%S ')
					return HttpResponse(json.dumps({'respuesta':'exito','fecha':fec}),mimetype='application/json')
				except Exception,e:
					print e
					return HttpResponse(json.dumps({'respuesta':'noSitio'}),mimetype='application/json')		
			else:
				return HttpResponse(json.dumps({'respuesta':'noCampos'}),mimetype='application/json')
		else:
			return HttpResponse(json.dumps({'respuesta':'noPOST'}),mimetype='application/json')
	else:
		return HttpResponse(json.dumps({'respuesta':'noAJAX'}),mimetype='application/json')

def busqueda(request):
	# import pdb
	# pdb.set_trace()
	language=obtener_idioma(request)
	url=resolver_url(request)
	if 'text_search' in request.POST:
		res = request.POST['text_search']
		pueblos=None
		eventos=None
		sitios=None
		relatos=None
		try:
			cont_pueblos= pueblo.objects.filter(NOMBRE__contains=res).count()
			if cont_pueblos >0:
				pueblos=pueblo.objects.filter(NOMBRE__contains=res)
				temp = []
				for pueb in pueblos:
					temp.append(pueb.get_pueblo_idioma(language))
				pueblos=temp
			cont_eventos=evento.objects.filter(NOMBRE__contains=res).count()
			if cont_eventos>0:
				eventos=evento.objects.filter(NOMBRE__contains=res)
				temp = []
				for even in eventos:
					temp.append(even.get_evento_idioma(language))
				eventos=temp
			cont_sitios=sitio_turistico.objects.filter(Q(NOMBRE__contains=res) | Q(DIRECCION__contains=res) | Q(DESCRIPCION__contains=res)).count()
			if cont_sitios>0:				
				cont_sitios=sitio_turistico.objects.filter(Q(NOMBRE__contains=res) | Q(DIRECCION__contains=res) | Q(DESCRIPCION__contains=res)).count()
				temp = []
				if cont_sitios >0:
					sitios=sitio_turistico.objects.filter(Q(NOMBRE__contains=res) | Q(DIRECCION__contains=res) | Q(DESCRIPCION__contains=res))
					for site in sitios:
						temp.append(site.get_sitio_turistico_idioma(language))
						sitios=temp		
			cont_relatos=relato.objects.filter(TITULO__contains=res).count()
			if cont_relatos>0:
				relatos=relato.objects.filter(TITULO__contains=res).count()
				temp = []
				for rel in relatos:
					temp.append(rel.get_sitio_relato_idioma(language))
				relatos=temp	
		except Exception,e:
			print e
		return render_to_response('busqueda.html',RequestContext(request,
			{'respuesta':res,
			'user':request.user,
			'pueblos':pueblos,
			'eventos':eventos,
			'sitios':sitios,
			'relatos':relatos,
			'url':url,
			}))
	else:
		return render_to_response('busqueda.html',RequestContext(request,
			{
			'user':request.user,
			'url':url,
			}))
	
def reporte_comentarios_ajax(request):
	# import pdb
	# pdb.set_trace()
	if request.is_ajax():
		if request.POST:
			if ('ID' in request.POST and 'TIPO_COMENTARIO' in request.POST and 'RAZON' in request.POST ):
				iden=request.POST['ID']
				tipo_comentario=request.POST['TIPO_COMENTARIO']
				razon = request.POST['RAZON']
				usuario=request.user
				try:
					fecha =datetime.datetime.now()
					reporte = reporte_comentario(CLASE_COMENTARIO=tipo_comentario,COMENTARIO=iden,RAZON=razon,FECHA=fecha,USUARIO=usuario)
					reporte.save()
					return HttpResponse(json.dumps({'respuesta':'exito'}),mimetype='application/json')
				except Exception,e:
					print e
					return HttpResponse(json.dumps({'respuesta':'fallido'}),mimetype='application/json')		
			else:
				return HttpResponse(json.dumps({'respuesta':'noCampos'}),mimetype='application/json')
		else:
			return HttpResponse(json.dumps({'respuesta':'noPOST'}),mimetype='application/json')
	else:
		return HttpResponse(json.dumps({'respuesta':'noAJAX'}),mimetype='application/json')

def enviar_relatos_ajax(request):
	# import pdb
	# pdb.set_trace()
	language=obtener_idioma(request)
	if request.is_ajax():
		if request.POST:
			if ('TITULO' in request.POST and 'RELATO' in request.POST  and 'PUEBLO' in request.POST):
				titulo=request.POST['TITULO']
				contenido=request.POST['RELATO']
				usuario=request.user
				nombre=request.POST['PUEBLO']
				village=pueblo.objects.get(NOMBRE=nombre)
				try:
					fecha =datetime.datetime.now()
					if language == settings.SELECTED_LANGUAGE:
						rel = relato(TITULO="",DESCRIPCION="",FECHA=fecha,USUARIO=usuario,PUEBLO=village,APROBADO=False,VALORACION=0)
						rel.save()
						rel_idiom=relato_idioma(TITULO=titulo,DESCRIPCION=contenido,RELATO=rel,IDIOMA=language)
						rel_idiom.save()
					else:
						rel = relato(TITULO=titulo,DESCRIPCION=contenido,FECHA=fecha,USUARIO=usuario,PUEBLO=village,APROBADO=False,VALORACION=0)
						rel.save()
					return HttpResponse(json.dumps({'respuesta':'exito'}),mimetype='application/json')
				except Exception,e:
					print e
					return HttpResponse(json.dumps({'respuesta':'fallido'}),mimetype='application/json')		
			else:
				return HttpResponse(json.dumps({'respuesta':'noCampos'}),mimetype='application/json')
		else:
			return HttpResponse(json.dumps({'respuesta':'noPOST'}),mimetype='application/json')
	else:
		return HttpResponse(json.dumps({'respuesta':'noAJAX'}),mimetype='application/json')

def mostrar_mas_comentarios_relatos_ajax(request):
	if request.is_ajax():
		if request.POST:
			if ('RELATO' in request.POST):
				iden=request.POST['ID']
				usuario=request.user
				try:
					rel=relato.objects.get(ID=iden)						
					comen_relato=comentario_relato.objects.filter(RELATOS=rel)
					dic['relato']=rel.ID
					objs = comentario_relato.objects.filter(RELATOS=rel)[3:]
					#dic['comentarios']=
					lista = []
					for obj in objs:
						dicc = {}
						dicc['usuario']=obj.USUARIO.username
						dicc['comentario']=obj.DESCRIPCION
						dicc['fecha']= obj.fecha.strftime('%d/%m/%Y, a las %H:%M:%S ')
						lista.append(dicc)
					dic['comentario']=lista
					return HttpResponse(json.dumps({'respuesta':'exito','comentarios':dic}),mimetype='application/json')
				except Exception,e:
					print e
					return HttpResponse(json.dumps({'respuesta':'noRelato'}),mimetype='application/json')		
			else:
				return HttpResponse(json.dumps({'respuesta':'noCampos'}),mimetype='application/json')
		else:
			return HttpResponse(json.dumps({'respuesta':'noPOST'}),mimetype='application/json')
	else:
		return HttpResponse(json.dumps({'respuesta':'noAJAX'}),mimetype='application/json')

# def es(request):
# 	process_request(request,'es-mx')
# 	return render_to_response('index.html',RequestContext(request,{'user':request.user,}))

# def en(request):
# 	import pdb
# 	pdb.set_trace()
# 	process_request(request,'en')
# 	return render_to_response('index.html',RequestContext(request,{'user':request.user,}))


#--------------------------------------------------------------------------->
def resolver_url(request):
	# import pdb
	# pdb.set_trace()
	cadena=None
	temp = request.get_full_path()
	cadena=''
	for language in settings.LANGUAGES:
		busca = language[0]
		try:
			indice=temp.rindex(busca+'/')
			if indice !=-1:
				indice += len(busca)
				cadena=temp[indice:len(temp)]
				break;
		except Exception,e:
			pass
	return cadena

def obtener_idioma(request):
	for language in settings.LANGUAGES:
		idioma = language[0]
		if idioma == request.LANGUAGE_CODE:
			return language[1]
	return ''