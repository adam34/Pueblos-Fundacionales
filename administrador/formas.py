# -*- encoding: utf-8 -*-
from django import forms
from administrador.models import *
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re
# from django.contrib.auth.forms import (UserCreationForm, UserChangeForm,
#     AdminPasswordChangeForm)

#Codigo extra de apoyo para los forms (como validaciones y colecciones de importancia)
def validar_usuario(valor):
	if len(valor) > 30:
		raise ValidationError(u'No debe ser mayor de 30 caractares.')
	if re.match(r'[\w]+$',valor) == None:
		raise ValidationError(u'Debe contener solamente números y caracteres, nada más.')
def validar_contrasena(valor):
	if len(valor) > 30:
		raise ValidationError(u'No debe ser mayor de 30 caractares.')
	if re.match(r'[\w]+$',valor) == None:
		raise ValidationError(u'Debe contener solamente números y caracteres, nada más.')

mensajes ={'required':'Error 101','max_length':'Error 102',}
	
#Codigo de los forms

class FormAutenticacion(forms.Form):
	Usuario=forms.CharField(required=True,help_text="Nombre de usuario.",max_length=20, error_messages=mensajes, validators=[validar_usuario])
	Contrasena=forms.CharField(widget=forms.PasswordInput,required=True,help_text="Nombre de usuario.",max_length=30,error_messages=mensajes, validators=[validar_contrasena])

class UserForm(forms.ModelForm):
	class Media:
		js = ('admin/js/users.js',)
		css = {}
	password2=forms.CharField(widget=forms.PasswordInput,required=True,help_text="Nombre de usuario.",max_length=30,error_messages=mensajes, validators=[validar_contrasena])
	class Meta:
		model=User
	def __init__(self, *args, **kwargs):
		super(UserForm, self).__init__(*args, **kwargs)
		self.fields['username'].help_text='Obligatorio. Longitud máxima de 30 caracteres alfanuméricos (letras y dígitos solamente).'
		self.fields['username'].validators=[validar_usuario]
		self.fields['username'].widget.attrs={'maxlength':'30',}
		self.fields['username'].widget.attrs={'class':'vTextField','maxlength':'30',}
		self.fields['username'].label='Usuario'

		self.fields['password'].validators=[validar_contrasena]
		self.fields['password'].help_text='Obligatorio. Longitud máxima de 30 caracteres'
		self.fields['password'].widget=forms.widgets.PasswordInput()
		self.fields['password'].widget.attrs={'maxlength':'30',}
		self.fields['password'].widget.attrs={'class':'vTextField','maxlength':'30',}
		self.fields['password'].label='Contraseña'

		self.fields['password2'].validators=[validar_contrasena]
		self.fields['password2'].help_text='Obligatorio. Vuelva a introducir la contraseña.'
		self.fields['password2'].widget=forms.widgets.PasswordInput()
		self.fields['password2'].widget.attrs={'maxlength':'30',}
		self.fields['password2'].widget.attrs={'class':'vTextField','maxlength':'30',}
		self.fields['password2'].label='Confirmar contraseña'

		self.fields['first_name'].label='Nombre(s)'
		self.fields['last_name'].label='Apellido(s)'
		self.fields['email'].label='Correo electrónico'

		self.fields['groups'].widget=forms.SelectMultiple()
		self.fields['groups'].widget.attrs = {'class':'input-xxlarge'}
		self.fields['user_permissions'].widget=forms.SelectMultiple()
		self.fields['user_permissions'].widget.attrs = {'class':'input-xxlarge',}


		# print self.fields['groups'].widget.attrs.keys()
		# print type(self.fields['groups'].widget.attrs)
		# print dir(self.fields['groups'].widget.attrs)

		self.fields['groups'].help_text='Los grupos a los que pertenece este usuario. Un usuario obtendrá todos los permisos concedidos para cada uno de su grupo. Mantenga presionada la tecla "Control", o "Command" en una Mac, para seleccionar más de una de las opciones.'
		self.fields['user_permissions'].help_text='Estos son permisos específicos para este usuario. Mantenga presionada "Control", o "Command" en una Mac, para seleccionar más de una de las opciones.'

class UserChangeForm(forms.ModelForm):
	class Meta:
		model=User
	def __init__(self, *args, **kwargs):
		super(UserChangeForm, self).__init__(*args, **kwargs)
		self.fields['username'].help_text=''
		self.fields['username'].widget.attrs={'maxlength':'30',}
		self.fields['username'].widget.attrs={'class':'vTextField','maxlength':'30','readonly':'true',}
		self.fields['username'].label='Usuario'

		self.fields['first_name'].label='Nombre(s)'
		self.fields['last_name'].label='Apellido(s)'
		self.fields['email'].label='Correo electrónico'
		
		self.fields['groups'].help_text='Los grupos a los que pertenece este usuario. Un usuario obtendrá todos los permisos concedidos para cada uno de su grupo. Mantenga presionada la tecla "Control", o "Command" en una Mac, para seleccionar más de una de las opciones.'
		self.fields['user_permissions'].help_text='Estos son permisos específicos para este usuario. Mantenga presionada "Control", o "Command" en una Mac, para seleccionar más de una de las opciones.'
		
#Codigo para el formulario del usuario
# class UserForm(UserCreationForm):
# 	def __init__(self, *args, **kwargs):
# 		super(UserForm, self).__init__(*args, **kwargs)

# 		self.fields['username'].help_text='Obligatorio. Longitud máxima de 30 caracteres alfanuméricos (letras y dígitos solamente).'
# 		self.fields['username'].validators=[validar_usuario]
# 		self.fields['username'].widget.attrs={'maxlength':'30',}
# 		self.fields['username'].widget.attrs={'class':'vTextField','maxlength':'30',}
# 		self.fields['username'].label='Usuario'

# 		self.fields['password1'].validators=[validar_contrasena]
# 		self.fields['password1'].help_text='Obligatorio. Longitud máxima de 30 caracteres'
# 		self.fields['password1'].widget=forms.widgets.PasswordInput()
# 		self.fields['password1'].widget.attrs={'maxlength':'30',}
# 		self.fields['password1'].widget.attrs={'class':'vTextField','maxlength':'30',}
# 		self.fields['password1'].label='Contraseña'

# 		self.fields['password2'].validators=[validar_contrasena]
# 		self.fields['password2'].help_text='Obligatorio. Vuelva a introducir la contraseña.'
# 		self.fields['password2'].widget=forms.widgets.PasswordInput()
# 		self.fields['password2'].widget.attrs={'maxlength':'30',}
# 		self.fields['password2'].widget.attrs={'class':'vTextField','maxlength':'30',}
# 		self.fields['password2'].label='Confirmar contraseña'
