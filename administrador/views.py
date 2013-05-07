# Create your views here.
import json
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response,redirect
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt

def vista1(request):
	return render_to_response('pagina1.html')

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