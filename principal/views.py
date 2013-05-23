# Create your views here.
# -*- encoding: utf-8 -*-
import json
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.models import User
from administrador.models import *


def home(request): 
	return render_to_response('index.html')

def secciones(request): 
	return render_to_response('secciones.html')

def pueblos(request): 
	return render_to_response('pueblos.html')

def galerias(request): 
	return render_to_response('galerias.html')

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

def eventos(request):
	eventos=evento.objects.all()
	return render_to_response('eventos.html',{'eventos':eventos})

def galeria(request):
	return render_to_response('multimedia/galeria.html')

def relatos(request):
	relatos = relato.objects.all()
	return render_to_response('relatos.html',{'relatos':relatos})

def sitiosT(request):
	sitios = sitio_turistico.objects.all()
	return render_to_response('sitios_turisticos.html',{'sitios':sitios})