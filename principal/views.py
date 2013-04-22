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