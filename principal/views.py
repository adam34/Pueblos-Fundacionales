# Create your views here.
# -*- encoding: utf-8 -*-
	# import pdb
	# pdb.set_trace()
import json
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.models import User
from django.conf import settings

from administrador.models import *
from django.views.decorators.csrf import csrf_exempt
from django.utils.translation import get_language_info,ugettext as _
from django.views import i18n
import json

def home(request): 
	# import pdb
	# pdb.set_trace()
	return render_to_response('index.html',RequestContext(request))

def login_ajax(request):
	pass

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
