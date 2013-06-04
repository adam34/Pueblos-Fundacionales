# Create your views here.
import json
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response,redirect
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from administrador.formas import *
from django.contrib.auth.models import User
from django.contrib import admin
from django.forms import *
from administrador.models import *

def acerca_de(request):
	return render_to_response('admin/acerca_de.html')

def config(request):
	# import pdb
	# pdb.set_trace()
	if request.user.is_authenticated():
		forma =ConfiguracionForm()
		return render_to_response('admin/config.html',RequestContext(request,{'user':request.user,'form':forma}))
	else:
		return redirect('admin/')

# def pueblos(request):
# 	dicc = {'user':request.user}
# 	if request.POST.__contains__('pueblos'):
# 		nombre = request.POST['pueblos']
# 		village = pueblo.objects.filter(NOMBRE= nombre)
# 		dicc['pueblos'] = nombre
# 		dicc['village'] = village
# 		return render_to_response('admin/pueblos.html',dicc)
# 	else:
# 		raise Http404




