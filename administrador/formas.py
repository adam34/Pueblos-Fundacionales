# -*- encoding: utf-8 -*-
from django import forms
from administrador.models import *
from django.contrib.auth.models import *
from django.core.exceptions import ValidationError
import re
from django.forms.util import ErrorList
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
#from django.contrib.admin.widgets import FilteredSelectMultiple
from administrador.extras.widgets import SelectMultipleCustom
from django.forms.widgets import *

#----------------------------------Validadores para UserForm------------------------------------------
def validar_usuario(valor):
	if len(valor) > 30:
		raise ValidationError(u'No debe ser mayor de 30 caracteres.')
	if len(valor) < 6:
		raise ValidationError(u'No debe ser menor de 6 caracteres.')
	if re.match(r'[\w]+$',valor) == None:
		raise ValidationError(u'Debe contener solamente números y caracteres, nada más.')
def validar_contrasena(valor):
	if len(valor) > 30 and len(valor) < 6:
		raise ValidationError(u'No debe ser menor de 6 y mayor de 30 caracteres.')
	if re.match(r'(?=.*\d)(?=.*[a-z])',valor) == None:
		raise ValidationError(u'Debe contener solamente números y caracteres, nada más.')
def validar_nombre(valor):
	if valor != '':
		if re.match(r'^([A-Za-zñÑáéíóúÁÉÍÓÚ]{3,})+((\s{1})[A-Za-zñÑáéíóúÁÉÍÓÚ]{3,})*$'.decode("utf-8"),valor) == None:
			raise ValidationError(u'El campo de nombre(s) no tiene el formato correcto. Asegurese de introducir nombres compuestos sólo por letras, de 3 caracteres como mínimo, separados por un "sólo" espacio y de proporcionar tanto el/los nombre(s) como el/los apellido(s).')
def validar_apellido(valor):
	if valor != "":
		if re.match(r'^([A-Za-zñÑáéíóúÁÉÍÓÚ]{3,})+((\s{1})[A-Za-zñÑáéíóúÁÉÍÓÚ]{3,})*$'.decode("utf-8"),valor) == None:
			raise ValidationError(u'El campo de apellido(s) no tiene el formato correcto. Asegurese de introducir nombres compuestos sólo por letras y separados por un "sólo" espacio y de proporcionar tanto el/los nombre(s) como el/los apellido(s).')
def validar_email(valor):
	if valor != "":
		if re.match(r'^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$',valor) == None:
			raise ValidationError(u'Debe contener solamente números y caracteres, nada más.')
#----------------------------------Fin de validadores para UserForm--------------------------------

mensajes ={'required':'El campo es obligatorio. No se puede dejar en blanco o sin datos','max_length':'El dato excedió el limite de caracteres para este campo',}

#------------------------------------------Codigo de los forms -------------------------------------------
errores_login={
	'min_length': ("Error del tipo min_length."),
	'max_length': ("Error del tipo max_length."),
}
class CustomAutenticacionForm(AuthenticationForm):
	username = forms.CharField(min_length=4,max_length=30,error_messages=errores_login)
	password = forms.CharField(min_length=4,max_length=30, widget=forms.PasswordInput,error_messages=errores_login)
	error_messages = {
		'invalid_login': ("Por favor de introducir un nombre de usuario y contraseña correctos. "
						"Considera que ambos campos son sensibles a mayusculas y minusculas."),
		'no_cookies': ("Tu navegador Web no parece tener la opción de cookies"
						"habilitada. Estas son necesarias para la identificación."),
		'inactive': ("Esta cuenta esta inactiva."),
		'no_staff': ("El usuario no tiene permisos para acceder al administrador."),
		}
	def clean(self):
		#super(CustomAutenticacionForm, self).clean()
		username = self.cleaned_data.get('username')
		password = self.cleaned_data.get('password')
		if username and password:
			self.user_cache = authenticate(username=username,
											password=password)
			if self.user_cache is None:
				raise forms.ValidationError(
					self.error_messages['invalid_login']
					)
			elif not self.user_cache.is_active:
				raise forms.ValidationError(self.error_messages['inactive'])
			elif not self.user_cache.is_staff:
				raise forms.ValidationError(self.error_messages['no_staff'])
		self.check_for_test_cookie()
		return self.cleaned_data

#-------------------------------Formularios para el modelo de users--------------------------------
class UserForm(forms.ModelForm):
	class Media:
		js = ('admin/js/users.js',)
		css = {}
	password2=forms.CharField(widget=forms.PasswordInput,required=True,help_text="Nombre de usuario.",max_length=30,error_messages=mensajes, validators=[validar_contrasena])
	class Meta:
		model=User
	def __init__(self, *args, **kwargs):
		#El campo username tiene sus propios validadores o metodos para validar el contenido del campo.
		super(UserForm, self).__init__(*args, **kwargs)
		self.fields['username'].help_text='Obligatorio. Longitud mínima de 6 y máxima de 30 caracteres alfanuméricos (letras y dígitos solamente).'
		self.fields['username'].validators=[validar_usuario]
		self.fields['username'].widget.attrs={'maxlength':'30',}
		self.fields['username'].widget.attrs={'class':'vTextField','maxlength':'30',}
		self.fields['username'].label='Usuario'

		self.fields['password'].validators=[validar_contrasena]
		self.fields['password'].help_text='Obligatorio. Longitud mínima de 6 y máxima de 30 caracteres'
		self.fields['password'].widget=forms.widgets.PasswordInput()
		self.fields['password'].widget.attrs={'maxlength':'30',}
		self.fields['password'].widget.attrs={'class':'vTextField','maxlength':'30',}
		self.fields['password'].label='Contraseña'

		self.fields['password2'].validators = []
		self.fields['password2'].help_text='Obligatorio. Vuelva a introducir la contraseña.'
		self.fields['password2'].widget=forms.widgets.PasswordInput()
		self.fields['password2'].widget.attrs={'maxlength':'30',}
		self.fields['password2'].widget.attrs={'class':'vTextField','maxlength':'30',}
		self.fields['password2'].label='Confirmar contraseña'

		self.fields['first_name'].validators = [validar_nombre]
		self.fields['first_name'].label='Nombre(s)'
		self.fields['first_name'].help_text='Opcional. Introduzca el/los nombre(s) compuestos solamente por caracteres, y separados por un espacio. Ejemplo: Luis Manuel.'
		self.fields['last_name'].validators = [validar_apellido]
		self.fields['last_name'].label='Apellido(s)'
		self.fields['last_name'].help_text='Opcional. Introduzca el/los nombre(s) compuestos solamente por caracteres, y separados por un espacio. Ejemplo: Ortega Rodriguez.'
		self.fields['email'].validators = [validar_email]
		self.fields['email'].label='Correo electrónico'
		self.fields['email'].help_text='Opcional. Ejemplo: username@server.com'

		
		# self.fields['groups'].widget=forms.MultipleChoiceField(queryset=Group.objects.all(), widget=FilteredSelectMultiple("Integrales", is_stacked=False))
		self.fields['groups'].widget = SelectMultipleCustom()
		self.fields['groups'].widget.attrs = {'class':'input-xxlarge'}
		self.fields['groups'].queryset= Group.objects.all()

		self.fields['user_permissions'].widget=SelectMultipleCustom()
		#self.fields['user_permissions'].widget.attrs = {'class':'input-xxlarge',}
		self.fields['user_permissions'].queryset=Permission.objects.all()

		self.fields['groups'].help_text='Los grupos a los que pertenece este usuario. Un usuario obtendrá todos los permisos concedidos para cada uno de su grupo. Mantenga presionada la tecla "Control", o "Command" en una Mac, para seleccionar más de una de las opciones.'
		self.fields['user_permissions'].help_text='Estos son permisos específicos para este usuario. Mantenga presionada "Control", o "Command" en una Mac, para seleccionar más de una de las opciones.'

	def save(self,commit=True):
		user = super(UserForm, self).save(commit=False)
		user.set_password(self.cleaned_data["password"])
		if commit:
			user.save(commit)
		return user

	def clean(self):
		super(UserForm, self).clean()
		cleaned_data = self.cleaned_data
		password1 = cleaned_data.get("password")
		password2 = cleaned_data.get("password2")
		if password1!=password2:
			if not self._errors.has_key('password2'):
				self._errors['password2']= ErrorList([u"Las contraseñas no pueden ser diferentes."])
				#raise ValidationError(u'Las contraseñas no pueden ser diferentes.')
		return cleaned_data

class UserChangeForm(forms.ModelForm):
	class Media:
		js = ('admin/js/users_change.js',)
		css = {}
	class Meta:
		model=User
	def __init__(self, *args, **kwargs):
		super(UserChangeForm, self).__init__(*args, **kwargs)
		self.fields['username'].help_text=''
		self.fields['username'].widget.attrs={'maxlength':'30',}
		self.fields['username'].widget.attrs={'class':'vTextField','maxlength':'30','readonly':'true',}
		self.fields['username'].label='Usuario'

		self.fields['first_name'].label='Nombre(s)'
		self.fields['first_name'].help_text='Opcional. Introduzca el/los nombre(s) compuestos solamente por caracteres, y separados por un espacio. Ejemplo: Luis Manuel.'
		self.fields['last_name'].label='Apellido(s)'
		self.fields['last_name'].help_text='Opcional. Introduzca el/los nombre(s) compuestos solamente por caracteres, y separados por un espacio. Ejemplo: Ortega Rodriguez.'
		self.fields['email'].label='Correo electrónico'
		self.fields['email'].help_text='Opcional. Ejemplo: username@server.com'

		self.fields['groups'].widget=forms.SelectMultiple()
		self.fields['groups'].widget.attrs = {'class':'input-xxlarge'}
		self.fields['user_permissions'].widget=forms.SelectMultiple()
		self.fields['user_permissions'].widget.attrs = {'class':'input-xxlarge',}

		self.fields['groups'].queryset= Group.objects.all()
		self.fields['user_permissions'].queryset=Permission.objects.all()

		self.fields['groups'].help_text='Los grupos a los que pertenece este usuario. Un usuario obtendrá todos los permisos concedidos para cada uno de su grupo. Mantenga presionada la tecla "Control", o "Command" en una Mac, para seleccionar más de una de las opciones.'
		self.fields['user_permissions'].help_text='Estos son permisos específicos para este usuario. Mantenga presionada "Control", o "Command" en una Mac, para seleccionar más de una de las opciones.'

#----------------------------Fin de formularios para el modelo de users-----------------------------

#--------------------------------Formularios para el modelo de groups---------------------------------
class GroupForm(forms.ModelForm):
	class Media:
		js = ('admin/js/groups.js',)
		css = {}
	class Meta:
		model=Group
	def __init__(self, *args, **kwargs):
		#El campo username tiene sus propios validadores o metodos para validar el contenido del campo.
		super(GroupForm, self).__init__(*args, **kwargs)
		self.fields['permissions'].widget= SelectMultipleCustom()
		self.fields['permissions'].queryset= Permission.objects.all()

		self.fields['permissions'].help_text='Estos son permisos específicos para este grupo. Mantenga presionada "Control", o "Command" en una Mac, para seleccionar más de una de las opciones.'

	def save(self,commit=True):
		pass

	def clean(self):
		pass

class GroupChangeForm(forms.ModelForm):
	class Media:
		js = ('admin/js/groups_change.js',)
		css = {}
	class Meta:
		model=Group
	def __init__(self, *args, **kwargs):
		#El campo username tiene sus propios validadores o metodos para validar el contenido del campo.
		super(GroupForm, self).__init__(*args, **kwargs)	
		# self.fields['groups'].widget=forms.MultipleChoiceField(queryset=Group.objects.all(), widget=FilteredSelectMultiple("Integrales", is_stacked=False))
		self.fields['name'].widget.attrs = {'disabled':'true'}


		self.fields['permissions'].widget = forms.SelectMultiple()
		self.fields['permissions'].widget.attrs = {'class':'input-xxlarge'}
		self.fields['permissions'].queryset= Permission.objects.all()

		self.fields['permissions'].help_text='Estos son permisos específicos para este grupo. Mantenga presionada "Control", o "Command" en una Mac, para seleccionar más de una de las opciones.'

	def save(self,commit=True):
		pass

	def clean(self):
		pass


#------------------------------Fin de formularios para el modelo de groups------------------------------