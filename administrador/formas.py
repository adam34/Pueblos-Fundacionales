# -*- encoding: utf-8 -*-
from django import forms
from administrador.models import *
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re

def validar_usuario(valor):
	if len(valor) > 20:
		raise ValidationError(u'No debe ser mayor de 20 caractares.')
	if re.match(r'[\w]+$',valor) == None:
		raise ValidationError(u'Debe contener solamente números y caracteres, nada más.')
def validar_contrasena(valor):
	if len(valor) > 30:
		raise ValidationError(u'No debe ser mayor de 30 caractares.')
	if re.match(r'[\w]+$',valor) == None:
		raise ValidationError(u'Debe contener solamente números y caracteres, nada más.')



mensajes ={'required':'Error 101','max_length':'Error 102',}
	
class FormAutenticacion(forms.Form):
	Usuario=forms.CharField(required=True,help_text="Nombre de usuario.",max_length=20, error_messages=mensajes, validators=[validar_usuario])
	Contrasena=forms.CharField(widget=forms.PasswordInput,required=True,help_text="Nombre de usuario.",max_length=30,error_messages=mensajes, validators=[validar_contrasena])

class FormUser(forms.ModelForm):
	class Meta:
		model = User