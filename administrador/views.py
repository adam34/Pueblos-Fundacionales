# Create your views here.
import json
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response,redirect
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from administrador.formas import *
from django.contrib.auth.models import User
from django.contrib import admin

def vista1(request):
	# import os
	# RUTA_PROYECTO = os.path.dirname(os.path.realpath(__file__))
	# print RUTA_PROYECTO
	# user=User.objects.get(username='root')
	# obj = UserForm(initial={'username':user.username,'password':user.password,'first_name':user.first_name,'last_name':user.last_name,'is_staff':user.is_staff,'is_superuser':user.is_superuser})
	obj = UserForm(initial={'password':'aaaa',})
	# print type(user.user_permissions.all())
	# print dir(user.user_permissions.all())
	# print user.user_permissions.all()
	# print type(admin.site.login_form)
	# print admin.site.login_form
	# print dir(admin.site.login_form)
	return render_to_response('pagina1.html',{'form':obj})

@csrf_exempt
def vista_ajax1(request):
	if request.is_ajax():
		print(request.POST)
		if "form" in request.POST:
			if "tipo" in request.POST:
				return HttpResponse("true2")
			else:
				return HttpResponse("false2")	
		else:
			return HttpResponse("false1")
	else:
		return HttpResponse("No datos para ti.")