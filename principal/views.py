# Create your views here.
import json
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext

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

def accesos(request): 
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