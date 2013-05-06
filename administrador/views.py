# Create your views here.
import json
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext

def vista1(request):
	var = [1,2,3,4,5]
	return render_to_response('pagina1.html',{'var':var})