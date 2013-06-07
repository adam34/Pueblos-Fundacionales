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
from administrador.extras.widgets import SelectMultipleCustom,MapInput,AccordionMultipleTextbox,AccordionMultiplesSimpleTextbox,VerInput
from django.forms.widgets import *
import datetime

	# import pdb
	# pdb.set_trace()

#----------------------------------Validadores------------------------------------------------
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


def validar_nombre_grupo(valor):
	if len(valor) > 30:
		raise ValidationError(u'No debe ser mayor de 30 caracteres.')
	if len(valor) < 4:
		raise ValidationError(u'No debe ser menor de 4 caracteres.')
	if re.match(r'[\w ]+$',valor) == None:
		raise ValidationError(u'Debe contener solamente números y caracteres, nada más.')

#----------------------------------Fin de validadores-----------------------------------------

#----------------------------------------Metodos especiales------------------------------------



#--------------------------------------Fin de metodos especiales-------------------------------

mensajes ={'required':'El campo es obligatorio. No se puede dejar en blanco o sin datos','max_length':'El dato excedió el limite de caracteres para este campo',}

#------------------------------------------Codigo de los forms ----------------------------------

class CustomAutenticacionForm(AuthenticationForm):
	errores_login={
		'min_length': ("No colocó la cantidad minima de caracteres para el campo."),
		'max_length': ("Excedió la cantidad máxima de caracteres para el campo."),
	}
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
		# import pdb
		# pdb.set_trace()
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
				self._errors['username']= ErrorList([u"El usuario no esta activo o ha sido bloqueado."])
			elif not self.user_cache.is_staff:
				self._errors['username']= ErrorList([u"El usuario no tiene permisos para acceder al administrador."])
			else:
				access=login()
				access.USUARIO=self.user_cache
				access.FECHA=datetime.datetime.now()
				self.check_for_test_cookie()
				try:
					access.save()
				except Exception,e:
					pass
		return self.cleaned_data

class ConfiguracionForm(forms.Form):
	NOMBRE_SITIO = forms.CharField(max_length=30,min_length=4,required=True, label='Nombre del sitio: ',help_text='Obligatorio. Texto que se mostrara como nombre del sitio')
	PIE_PAGINA = forms.CharField(max_length=30,min_length=4,required=True, label='Pie de pagina: ',help_text='Obligatorio.Texto que se mostrara en el pie de la pagina del sitio')
	COMENTARIOS_SITIOS=forms.BooleanField(initial=True, label='Comentarios para sitios: ')
	COMENTARIOS_PUEBLOS=forms.BooleanField(initial=True, label='Comentarios para pueblos: ')
	COMENTARIOS_EVENTOS=forms.BooleanField(initial=True, label='Comentarios para eventos: ')
	COMENTARIOS_RELATOS=forms.BooleanField(initial=True, label='Comentarios para relatos: ')
	# class Meta:
		# model=pueblo
	# def __init__(self, *args, **kwargs):
		#El campo username tiene sus propios validadores o metodos para validar el contenido del campo.
		# super(PuebloChangeForm, self).__init__(*args, **kwargs)
		# self.fields['permissions'].widget= SelectMultipleCustom()
		# self.fields['permissions'].queryset= Permission.objects.all()

		# self.fields['permissions'].help_text='Estos son permisos específicos para este grupo. Mantenga presionada "Control", o "Command" en una Mac, para seleccionar más de una de las opciones.'

	# def save(self,commit=True):
	# 	pass

	# def clean(self):
	# 	pass


#-------------------------------Formularios para el modelo de users--------------------------------
class UserForm(forms.ModelForm):
	password2=forms.CharField(widget=forms.PasswordInput,required=True,help_text="Nombre de usuario.",max_length=30,error_messages=mensajes, validators=[validar_contrasena])
	class Media:
		# css={'all':('admin/css/multi-select.css',),}
		js=('admin/js/users.js',)
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


		self.fields['groups'].widget = SelectMultipleCustom()
		# self.fields['groups'].widget.attrs = {'class':'input-xxlarge'}
		self.fields['groups'].queryset= Group.objects.all()

		self.fields['user_permissions'].widget=SelectMultipleCustom()
		#self.fields['user_permissions'].widget.attrs = {'class':'input-xxlarge',}
		self.fields['user_permissions'].queryset=Permission.objects.all()

		self.fields['is_active'].help_text=' Especifica si el usuario esta activo o bloqueado'

		self.fields['groups'].help_text='Los grupos a los que pertenece este usuario. Un usuario obtendrá todos los permisos concedidos para cada uno de su grupo. Seleccione los grupos o el grupo en el que desea asignarle.'
		self.fields['user_permissions'].help_text='Estos son permisos específicos para este usuario. Seleccione los grupos o el grupo en el que desea asignarle.'

	def save(self,commit=True):
		# import pdb
		# pdb.set_trace()
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
	class Meta:
		model=User
	class Media:
		# css={'all':('/static/admin/css/multi-select.css',),}
		js=('admin/js/users.js',)
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

		self.fields['groups'].widget=SelectMultipleCustom()
		self.fields['groups'].widget.attrs = {'class':'input-xxlarge'}
		self.fields['user_permissions'].widget=SelectMultipleCustom()
		self.fields['user_permissions'].widget.attrs = {'class':'input-xxlarge',}

		self.fields['groups'].queryset= Group.objects.all()
		self.fields['user_permissions'].queryset=Permission.objects.all()

		self.fields['groups'].help_text='Los grupos a los que pertenece este usuario. Un usuario obtendrá todos los permisos concedidos para cada uno de su grupo. Seleccione los grupos o el grupo en el que desea asignarle.'
		self.fields['user_permissions'].help_text='Estos son permisos específicos para este usuario. Seleccione los grupos o el grupo en el que desea asignarle.'
	
	def save(self,commit=True):
		# import pdb
		# pdb.set_trace()
		user = super(UserChangeForm, self).save(commit=False)
		if commit:
			user.save(commit)
		return user

	def clean(self):
		super(UserChangeForm, self).clean()
		cleaned_data = self.cleaned_data
		return cleaned_data


#----------------------------Fin de formularios para el modelo de users-----------------------------

#--------------------------------Formularios para el modelo de groups---------------------------------
class GroupForm(forms.ModelForm):
	class Meta:
		model=Group
	class Media:
		js=('admin/js/grupos.js',)
	def __init__(self, *args, **kwargs):
		#El campo username tiene sus propios validadores o metodos para validar el contenido del campo.
		super(GroupForm, self).__init__(*args, **kwargs)
		self.fields['name'].help_text="Obligatorio. Nombre del grupo. Se aceptan sólo letras con un solo espacio de separación entre las palabras y longitud mínima de 4 y máxima de 30 caracteres."
		self.fields['name'].validators=[validar_nombre_grupo];
		self.fields['permissions'].widget= SelectMultipleCustom()
		self.fields['permissions'].queryset= Permission.objects.all()
		self.fields['permissions'].help_text='Estos son permisos específicos para este grupo. Seleccione los permisos que desee darle a este grupo haciendo clic sobre ellos.'

	def save(self,commit=True):
		# import pdb
		# pdb.set_trace()
		grupo = super(GroupForm, self).save(commit=False)
		if commit:
			grupo.save(commit)
		return grupo


	def clean(self):
		super(GroupForm, self).clean()
		cleaned_data = self.cleaned_data
		return cleaned_data

class GroupChangeForm(forms.ModelForm):
	class Meta:
		model=Group
	class Media:
		#css={'all':('admin/css/multi-select.css',),}
		js=('admin/js/grupos.js',)
	def __init__(self, *args, **kwargs):
		#El campo username tiene sus propios validadores o metodos para validar el contenido del campo.
		super(GroupChangeForm, self).__init__(*args, **kwargs)
		self.fields['name'].widget.attrs = {'readonly':'true'}
		self.fields['name'].validators=[validar_nombre_grupo];
		self.fields['permissions'].widget= SelectMultipleCustom()
		self.fields['permissions'].queryset= Permission.objects.all()

		self.fields['permissions'].help_text='Estos son permisos específicos para este grupo. Seleccione los permisos que desee darle a este grupo haciendo clic sobre ellos.'

	def save(self,commit=True):
		# import pdb
		# pdb.set_trace()
		grupo = super(GroupChangeForm, self).save(commit=False)
		if commit:
			grupo.save(commit)
		return grupo


	def clean(self):
		super(GroupChangeForm, self).clean()
		cleaned_data = self.cleaned_data
		return cleaned_data

#------------------------------Fin de formularios para el modelo de groups-----------------------


#------------------------------Formularios para el modelo de pueblos-----------------------------

class PuebloForm(forms.ModelForm):
	# ADMINISTRADORES = forms.ModelMultipleChoiceField(label='Administradores ',queryset = User.objects.exclude(username='root'), widget = SelectMultipleCustom())
	HISTORIA = forms.CharField(required=False)
	CULTURA = forms.CharField(required=False)
	COMIDA = forms.CharField(required=False)
	DATOS = forms.CharField(required=False)
	MAPA = forms.CharField(required=False)
	LATITUD = forms.CharField(required=False)
	LONGITUD = forms.CharField(required=False)
	class Media:
		#css={'all':('admin/css/multi-select.css',),}
		js=('admin/js/pueblos.js','tinymce/js/tinymce/tinymce.min.js')
	class Meta:
		model=pueblo
	def __init__(self, *args, **kwargs):
		#El campo username tiene sus propios validadores o metodos para validar el contenido del campo.
		super(PuebloForm, self).__init__(*args, **kwargs)
		self.fields['NOMBRE'].help_text= "Obligatorio. Nombre del pueblo a registrar."
		self.fields['TIPO'].help_text= "Obligatorio. Clase de pueblo a registrar en el sistema."
		# import pdb
		# pdb.set_trace()
		#self.fields['ADMINISTRADORES'].widget = SelectMultipleCustom()
		#self.fields['ADMINISTRADORES'].queryset = User.objects.exclude(username='root')

		self.fields['HISTORIA'].widget=AccordionMultipleTextbox()
		self.fields['CULTURA'].widget=AccordionMultipleTextbox()
		self.fields['COMIDA'].widget=AccordionMultipleTextbox()
		self.fields['DATOS'].widget=AccordionMultipleTextbox()
		self.fields['HISTORIA'].widget.attrs = {'rows':'10','class':'vTextField span10','maxlength':'1500'}
		self.fields['HISTORIA'].help_text='No más de 1500 caracteres.'

		self.fields['CULTURA'].widget.attrs = {'rows':'10','class':'vTextField span10','maxlength':'1500'}
		self.fields['CULTURA'].help_text='No más de 1500 caracteres.'

		self.fields['COMIDA'].widget.attrs = {'rows':'10','class':'vTextField span10','maxlength':'1500'}
		self.fields['COMIDA'].help_text='No más de 1500 caracteres.'
		
		self.fields['DATOS'].widget.attrs = {'rows':'10','class':'vTextField span10','maxlength':'1500'}
		self.fields['DATOS'].help_text='No más de 1500 caracteres.'

		self.fields['LATITUD'].widget = HiddenInput()
		self.fields['LONGITUD'].widget = HiddenInput()
		self.fields['MAPA'].widget = MapInput(attrs={'type':'text',"class":"span12 vTextField"})

	def save(self,commit=True):
		# import pdb
		# pdb.set_trace()
		pueblo = super(PuebloForm, self).save(commit=False)
		pueblo.HISTORIA=self.data['HISTORIA']
		pueblo.CULTURA=self.data['CULTURA']
		pueblo.COMIDA=self.data['COMIDA']
		pueblo.DATOS=self.data['DATOS']
		# if commit:
		# 	pueblo.save(commit)
		pueblo.save()

		for idioma in IDIOMAS:
			nombre="HISTORIA_"+idioma[0]
			historia=""
			cultura=""
			comida=""
			datos=""
			if self.data.__contains__(nombre):
				historia=self.data[nombre]
			nombre="CULTURA_"+idioma[0]
			if self.data.__contains__(nombre):
				cultura=self.data[nombre]
			nombre="COMIDA_"+idioma[0]
			if self.data.__contains__(nombre):
				comida=self.data[nombre]
			nombre="DATOS_"+idioma[0]
			if self.data.__contains__(nombre):
				datos=self.data[nombre]
			
			if (historia != "" or cultura !="" or comida != "" or datos !=""):
				pueb_idiom = pueblo_idioma()
				pueb_idiom.PUEBLO = pueblo
				pueb_idiom.IDIOMA = idioma[0]
				pueb_idiom.HISTORIA = historia
				pueb_idiom.CULTURA = cultura
				pueb_idiom.COMIDA = comida
				pueb_idiom.DATOS = datos
				pueb_idiom.save(commit)
			#HISTORIA
			#CULTURA
			#COMIDAS
			#DATOS
		return pueblo

	def clean(self):
		super(PuebloForm, self).clean()
		cleaned_data = self.cleaned_data

		latitud = cleaned_data["LATITUD"]
		if latitud !="":
			if re.match(r'([-]?)([0-9]{1,3})[.]([0-9]{1,16})$',latitud) == None:
				self._errors['MAPA']= ErrorList([u"Ocurrió un error interno con el formato de la latitud. Favor de contactar al administrador."])
		longitud = cleaned_data["LONGITUD"]
		if longitud !="":
			if re.match(r'([-]?)([0-9]{1,3})[.]([0-9]{1,16})$',longitud) == None:
				if not self._errors.has_key('MAPA'):
					self._errors['MAPA']= ErrorList([u"Ocurrió un error interno con el formato de la latitud. Favor de contactar al administrador."])
		administrador = cleaned_data['ADMINISTRADOR']

		try:
			if not administrador.is_staff:
				self._errors['ADMINISTRADOR']= ErrorList([u"No puede ser asignado un usuario como administrador de un pueblo sino tiene acceso al administrador."])
		except User.DoesNotExist,e:
			print e
			self._errors['ADMINISTRADOR']= ErrorList([u"No puede ser asignado un usuario como administrador sino existe."])
		return cleaned_data

class PuebloChangeForm(forms.ModelForm):
	HISTORIA = forms.CharField(required=False)
	CULTURA = forms.CharField(required=False)
	COMIDA = forms.CharField(required=False)
	DATOS = forms.CharField(required=False)
	MAPA = forms.CharField(required=False)
	LATITUD = forms.CharField(required=False)
	LONGITUD = forms.CharField(required=False)
	class Meta:
		model=pueblo
	class Media:
		#css={'all':('admin/css/multi-select.css',),}
		js=('admin/js/pueblos.js','tinymce/js/tinymce/tinymce.min.js')
	def __init__(self, *args, **kwargs):
		#El campo username tiene sus propios validadores o metodos para validar el contenido del campo.
		super(PuebloChangeForm, self).__init__(*args, **kwargs)
		self.fields['NOMBRE'].help_text= "Obligatorio. Nombre del pueblo a registrar."
		self.fields['NOMBRE'].widget.attrs = {'readonly':'true'}
		self.fields['TIPO'].help_text= "Obligatorio. Clase de pueblo a registrar en el sistema."
		# import pdb
		# pdb.set_trace()

		obj = kwargs['instance']
		historia = {u'Español' : obj.HISTORIA}
		cultura = {u'Español' : obj.CULTURA}
		datos = {u'Español' : obj.DATOS}
		comida = {u'Español': obj.COMIDA}
		try:
			pueb_idioms=pueblo_idioma.objects.get(PUEBLO=obj)
			if isinstance(pueb_idioms,pueblo_idioma):
				historia[u''+pueb_idioms.IDIOMA]=pueb_idioms.HISTORIA
				cultura[u''+pueb_idioms.IDIOMA]=pueb_idioms.CULTURA
				datos[u''+pueb_idioms.IDIOMA]=pueb_idioms.DATOS
				comida[u''+pueb_idioms.IDIOMA]=pueb_idioms.COMIDA
			elif isinstance(pueb_idioms,list):
				for pueb_idiom in pueb_idioms:
					historia[pueb_idiom.IDIOMA]=pueb_idiom.HISTORIA
					cultura[pueb_idiom.IDIOMA]=pueb_idiom.CULTURA
					datos[pueb_idiom.IDIOMA]=pueb_idiom.DATOS
					comida[pueb_idiom.IDIOMA]=pueb_idiom.COMIDA	
		except pueblo_idioma.DoesNotExist,e:
			pass
		self.fields['HISTORIA'].widget=AccordionMultipleTextbox(data=historia)
		self.fields['CULTURA'].widget=AccordionMultipleTextbox(data=cultura)
		self.fields['COMIDA'].widget=AccordionMultipleTextbox(data=comida)
		self.fields['DATOS'].widget=AccordionMultipleTextbox(data=datos)
		self.fields['HISTORIA'].widget.attrs = {'rows':'10','class':'vTextField span10','maxlength':'1500'}
		self.fields['HISTORIA'].help_text='No más de 1500 caracteres.'

		self.fields['CULTURA'].widget.attrs = {'rows':'10','class':'vTextField span10','maxlength':'1500'}
		self.fields['CULTURA'].help_text='No más de 1500 caracteres.'

		self.fields['COMIDA'].widget.attrs = {'rows':'10','class':'vTextField span10','maxlength':'1500'}
		self.fields['COMIDA'].help_text='No más de 1500 caracteres.'

		self.fields['DATOS'].widget.attrs = {'rows':'10','class':'vTextField span10','maxlength':'1500'}
		self.fields['DATOS'].help_text='No más de 1500 caracteres.'

		self.fields['LATITUD'].widget = HiddenInput()
		self.fields['LONGITUD'].widget = HiddenInput()
		coordenadas= {}
		if (obj.LATITUD is not None and obj.LONGITUD is not None):
			coordenadas['LATITUD'] = obj.LATITUD
			coordenadas['LONGITUD'] = obj.LONGITUD
		else:
			coordenadas['LATITUD'] = ""
			coordenadas['LONGITUD'] = ""
		self.fields['MAPA'].widget = MapInput(attrs={'type':'text',"class":"span12 vTextField"},data=coordenadas)

	def save(self,commit=True):
		pueblo = super(PuebloForm, self).save(commit=False)
		pueblo.HISTORIA=self.data['HISTORIA']
		pueblo.CULTURA=self.data['CULTURA']
		pueblo.COMIDA=self.data['COMIDA']
		pueblo.DATOS=self.data['DATOS']
		# if commit:
		# 	pueblo.save(commit)
		pueblo.save()

		for idioma in IDIOMAS:
			nombre="HISTORIA_"+idioma[0]
			historia=""
			cultura=""
			comida=""
			datos=""
			if self.data.__contains__(nombre):
				historia=self.data[nombre]
			nombre="CULTURA_"+idioma[0]
			if self.data.__contains__(nombre):
				cultura=self.data[nombre]
			nombre="COMIDA_"+idioma[0]
			if self.data.__contains__(nombre):
				comida=self.data[nombre]
			nombre="DATOS_"+idioma[0]
			if self.data.__contains__(nombre):
				datos=self.data[nombre]
			
			if (historia != "" or cultura !="" or comida != "" or datos !=""):
				pueb_idiom = pueblo_idioma()
				pueb_idiom.PUEBLO = pueblo
				pueb_idiom.IDIOMA = idioma[0]
				pueb_idiom.HISTORIA = historia
				pueb_idiom.CULTURA = cultura
				pueb_idiom.COMIDA = comida
				pueb_idiom.DATOS = datos
				pueb_idiom.save(commit)
		return pueblo


	def clean(self):
		super(PuebloChangeForm, self).clean()
		cleaned_data = self.cleaned_data

		latitud = cleaned_data["LATITUD"]
		if latitud !="":
			if re.match(r'([-]?)([0-9]{1,3})[.]([0-9]{1,16})$',latitud) == None:
				self._errors['MAPA']= ErrorList([u"Ocurrió un error interno con el formato de la latitud. Favor de contactar al administrador."])
		longitud = cleaned_data["LONGITUD"]
		if longitud !="":
			if re.match(r'([-]?)([0-9]{1,3})[.]([0-9]{1,16})$',longitud) == None:
				if not self._errors.has_key('MAPA'):
					self._errors['MAPA']= ErrorList([u"Ocurrió un error interno con el formato de la latitud. Favor de contactar al administrador."])
		administrador = cleaned_data['ADMINISTRADOR']
		try:
			if not administrador.is_staff:
				self._errors['ADMINISTRADOR']= ErrorList([u"No puede ser asignado un usuario como administrador de un pueblo sino tiene acceso al administrador."])
		except User.DoesNotExist,e:
			print e
			self._errors['ADMINISTRADOR']= ErrorList([u"No puede ser asignado un usuario como administrador sino existe."])
		return cleaned_data

#------------------------------Fin de formularios para el modelo de pueblos----------------------


#------------------------------Formularios para el modelo de curiosidades------------------------

class CuriosidadesForm(forms.ModelForm):
	# ADMINISTRADORES = forms.ModelMultipleChoiceField(label='Administradores ',queryset = User.objects.exclude(username='root'), widget = SelectMultipleCustom())
	class Media:
		#css={'all':('admin/css/multi-select.css',),}
		js=('admin/js/curiosidades.js',)
	class Meta:
		model=curiosidad
	def __init__(self, *args, **kwargs):
		#El campo username tiene sus propios validadores o metodos para validar el contenido del campo.
		super(CuriosidadesForm, self).__init__(*args, **kwargs)
		self.fields['PUEBLO'].help_text= "Obligatorio. Nombre del pueblo a asociar."
		self.fields['TITULO'].help_text= "Obligatorio. Encabezado de la curiosidad. El idioma original es obligatorio. No más de 2000 caracteres."
		self.fields['DESCRIPCION'].help_text= "Obligatorio. Contenido de la curiosidad. El idioma original es obligatorio. No más de 2000 caracteres."
		self.fields['TITULO'].widget=AccordionMultiplesSimpleTextbox(attrs={'maxlength':'30'})

		self.fields['DESCRIPCION'].widget=AccordionMultipleTextbox(attrs = {'rows':'10','class':'vTextField span10','maxlength':'2000'})
		# import pdb
		# pdb.set_trace()
		#self.fields['ADMINISTRADORES'].widget = SelectMultipleCustom()
		#self.fields['ADMINISTRADORES'].queryset = User.objects.exclude(username='root')

	def save(self,commit=True):
		# import pdb
		# pdb.set_trace()
		curiosidad = super(CuriosidadesForm, self).save(commit=False)
		curiosidad.save()

		for idioma in IDIOMAS:
			titulo=""
			descripcion=""
			nombre="TITULO_"+idioma[0]
			if self.data.__contains__(nombre):
				titulo=self.data[nombre]
			nombre="DESCRIPCION_"+idioma[0]
			if self.data.__contains__(nombre):
				descripcion=self.data[nombre]
			
			if (titulo != "" or descripcion !=""):
				cur_idiom = curiosidad_idioma()
				cur_idiom.CURIOSIDAD = curiosidad
				cur_idiom.IDIOMA= idioma[0]
				cur_idiom.TITULO = titulo
				cur_idiom.DESCRIPCION = descripcion
				cur_idiom.save(commit)
		return curiosidad

	def clean(self):
		# import pdb
		# pdb.set_trace()
		super(CuriosidadesForm, self).clean()
		cleaned_data = self.cleaned_data
		return cleaned_data

class CuriosidadesChangeForm(forms.ModelForm):
	class Meta:
		model=curiosidad
	class Media:
		#css={'all':('admin/css/multi-select.css',),}
		js=('admin/js/curiosidades.js',)
	def __init__(self, *args, **kwargs):
		#El campo username tiene sus propios validadores o metodos para validar el contenido del campo.
		super(CuriosidadesChangeForm, self).__init__(*args, **kwargs)
		self.fields['PUEBLO'].help_text= "Obligatorio. Nombre del pueblo a asociar."
		self.fields['TITULO'].help_text= "Obligatorio. Encabezado de la curiosidad. El idioma original es obligatorio. No más de 2000 caracteres."
		self.fields['DESCRIPCION'].help_text= "Obligatorio. Contenido de la curiosidad. El idioma original es obligatorio. No más de 2000 caracteres."
		# import pdb
		# pdb.set_trace()

		obj = kwargs['instance']
		titulo = {u'Español' : obj.TITULO}
		descripcion = {u'Español' : obj.DESCRIPCION}
		try:
			curs_idioms=curiosidad_idioma.objects.get(CURIOSIDAD=obj)
			if isinstance(curs_idioms,curiosidad_idioma):
				titulo[u''+curs_idioms.IDIOMA]=curs_idioms.TITULO
				descripcion[u''+curs_idioms.IDIOMA]=curs_idioms.DESCRIPCION
			elif isinstance(curs_idioms,list):
				for cur_idioms in curs_idioms:
					titulo[cur_idioms.IDIOMA]=cur_idioms.TITULO
					descripcion[cur_idioms.IDIOMA]=cur_idioms.DESCRIPCION
		except curiosidad_idioma.DoesNotExist,e:
			pass
		self.fields['TITULO'].widget=AccordionMultiplesSimpleTextbox(data=titulo)
		self.fields['DESCRIPCION'].widget=AccordionMultipleTextbox(attrs = {'rows':'10','class':'vTextField span10','maxlength':'2000'},data=descripcion)

	def save(self,commit=True):
		# import pdb
		# pdb.set_trace()
		curiosidad = super(CuriosidadesChangeForm, self).save(commit=False)
		curiosidad.save()

		for idioma in IDIOMAS:
			titulo=""
			descripcion=""
			nombre="TITULO_"+idioma[0]
			if self.data.__contains__(nombre):
				titulo=self.data[nombre]
			nombre="DESCRIPCION_"+idioma[0]
			if self.data.__contains__(nombre):
				descripcion=self.data[nombre]
			
			if (titulo != "" or descripcion !=""):
				cur_idiom = curiosidad_idioma()
				cur_idiom.CURIOSIDAD = curiosidad
				cur_idiom.IDIOMA= idioma[0]
				cur_idiom.TITULO = titulo
				cur_idiom.DESCRIPCION = descripcion
				cur_idiom.save(commit)
		return curiosidad


	def clean(self):
		# import pdb
		# pdb.set_trace()
		super(CuriosidadesChangeForm, self).clean()
		cleaned_data = self.cleaned_data
		return cleaned_data

#------------------------------Fin de formularios para el modelo de curiosidades-----------------




#------------------------------Formularios para el modelo de eventos------------------------

class EventosForm(forms.ModelForm):
	MAPA = forms.CharField(required=False)
	LATITUD = forms.CharField(required=False)
	LONGITUD = forms.CharField(required=False)
	# ADMINISTRADORES = forms.ModelMultipleChoiceField(label='Administradores ',queryset = User.objects.exclude(username='root'), widget = SelectMultipleCustom())
	class Media:
		#css={'all':('admin/css/multi-select.css',),}
		js=('admin/js/eventos.js',)
	class Meta:
		model=evento
	def __init__(self, *args, **kwargs):
		#El campo username tiene sus propios validadores o metodos para validar el contenido del campo.
		super(EventosForm, self).__init__(*args, **kwargs)
		self.fields['NOMBRE'].help_text= "Obligatorio. Nombre del evento."
		self.fields['FECHA'].help_text= "Obligatorio. Formato dd/mm/yyyy Y hh:mm:ss formato 24hrs."
		self.fields['PUEBLO'].help_text= "Obligatorio. Pueblo donde se llevará acabo el evento."
		self.fields['DESCRIPCION'].help_text= "Obligatorio. Información acerca del evento. No más de 2000 caracteres."
		self.fields['LUGAR'].help_text= "Obligatorio. Ubicación exacta donde se llevará exacto el evento. No más de 200 caracteres."

		self.fields['DESCRIPCION'].widget=AccordionMultipleTextbox(attrs = {'rows':'10','class':'vTextField span10','maxlength':'2000'})
		self.fields['LUGAR'].widget=AccordionMultiplesSimpleTextbox(attrs={'maxlength':'200','rows':'3'})

		self.fields['LATITUD'].widget = HiddenInput()
		self.fields['LONGITUD'].widget = HiddenInput()
		self.fields['MAPA'].widget = MapInput(attrs={'type':'text',"class":"span12 vTextField"})
		self.fields['IMAGEN'].required = False




	def save(self,commit=True):
		# import pdb
		# pdb.set_trace()
		evento = super(EventosForm, self).save(commit=False)
		evento.save()

		for idioma in IDIOMAS:			
			lugar=""
			descripcion=""
			nombre="LUGAR_"+idioma[0]
			if self.data.__contains__(nombre):
				lugar=self.data[nombre]
			nombre="DESCRIPCION_"+idioma[0]
			if self.data.__contains__(nombre):
				descripcion=self.data[nombre]
			
			if (lugar != "" or descripcion !=""):
				event_idiom = evento_idioma()
				event_idiom.EVENTO = evento
				event_idiom.IDIOMA= idioma[0]
				event_idiom.LUGAR = lugar
				event_idiom.DESCRIPCION = descripcion
				event_idiom.save(commit)
		return evento

	def clean(self):
		# import pdb
		# pdb.set_trace()
		super(EventosForm, self).clean()
		cleaned_data = self.cleaned_data
		latitud = cleaned_data["LATITUD"]
		if latitud !="":
			if re.match(r'([-]?)([0-9]{1,3})[.]([0-9]{1,16})$',latitud) == None:
				self._errors['MAPA']= ErrorList([u"Ocurrió un error interno con el formato de la latitud. Favor de contactar al administrador."])
		longitud = cleaned_data["LONGITUD"]
		if longitud !="":
			if re.match(r'([-]?)([0-9]{1,3})[.]([0-9]{1,16})$',longitud) == None:
				if not self._errors.has_key('MAPA'):
					self._errors['MAPA']= ErrorList([u"Ocurrió un error interno con el formato de la latitud. Favor de contactar al administrador."])
		return cleaned_data

class EventosChangeForm(forms.ModelForm):
	MAPA = forms.CharField(required=False)
	LATITUD = forms.CharField(required=False)
	LONGITUD = forms.CharField(required=False)
	class Meta:
		model=evento
	class Media:
		#css={'all':('admin/css/multi-select.css',),}
		js=('admin/js/eventos.js',)
	def __init__(self, *args, **kwargs):
		#El campo username tiene sus propios validadores o metodos para validar el contenido del campo.
		super(EventosChangeForm, self).__init__(*args, **kwargs)
		self.fields['NOMBRE'].widget.attrs = {'readonly':'true'}
		self.fields['FECHA'].help_text= "Obligatorio. Formato dd/mm/yyyy Y hh:mm:ss formato 24hrs."
		self.fields['PUEBLO'].help_text= "Obligatorio. Pueblo donde se llevará acabo el evento."

		self.fields['LATITUD'].widget = HiddenInput()
		self.fields['LONGITUD'].widget = HiddenInput()
		self.fields['MAPA'].widget = MapInput(attrs={'type':'text',"class":"span12 vTextField"})
		self.fields['IMAGEN'].required = False

		obj = kwargs['instance']
		lugar = {u'Español' : obj.LUGAR}
		descripcion = {u'Español' : obj.DESCRIPCION}
		try:
			events_idioms=evento_idioma.objects.get(EVENTO=obj)
			if isinstance(events_idioms,evento_idioma):
				lugar[u''+events_idioms.IDIOMA]=events_idioms.LUGAR
				descripcion[u''+events_idioms.IDIOMA]=events_idioms.DESCRIPCION
			elif isinstance(events_idioms,list):
				for event_idioms in events_idioms:
					lugar[event_idioms.IDIOMA]=event_idioms.LUGAR
					descripcion[event_idioms.IDIOMA]=event_idioms.DESCRIPCION
		except evento_idioma.DoesNotExist,e:
			pass

		self.fields['DESCRIPCION'].widget=AccordionMultipleTextbox(attrs = {'rows':'10','class':'vTextField span10','maxlength':'2000'},data=descripcion)
		self.fields['LUGAR'].widget=AccordionMultiplesSimpleTextbox(attrs={'maxlength':'200','rows':'3'},data=lugar)
		self.fields['DESCRIPCION'].help_text= "Obligatorio. Información acerca del evento. No más de 2000 caracteres."
		self.fields['LUGAR'].help_text= "Obligatorio. Ubicación exacta donde se llevará exacto el evento. No más de 200 caracteres."


		self.fields['LATITUD'].widget = HiddenInput()
		self.fields['LONGITUD'].widget = HiddenInput()
		coordenadas= {}
		if (obj.LATITUD is not None and obj.LONGITUD is not None):
			coordenadas['LATITUD'] = obj.LATITUD
			coordenadas['LONGITUD'] = obj.LONGITUD
		else:
			coordenadas['LATITUD'] = ""
			coordenadas['LONGITUD'] = ""
		self.fields['MAPA'].widget = MapInput(attrs={'type':'text',"class":"span12 vTextField"},data=coordenadas)

	def save(self,commit=True):
		# import pdb
		# pdb.set_trace()
		evento = super(EventosChangeForm, self).save(commit=False)
		evento.save()

		for idioma in IDIOMAS:
			
			lugar=""
			descripcion=""
			nombre="LUGAR_"+idioma[0]
			if self.data.__contains__(nombre):
				lugar=self.data[nombre]
			nombre="DESCRIPCION_"+idioma[0]
			if self.data.__contains__(nombre):
				descripcion=self.data[nombre]
			
			if (lugar != "" or descripcion !=""):
				event_idiom = evento_idioma()
				event_idiom.EVENTO = evento
				event_idiom.IDIOMA= idioma[0]
				event_idiom.LUGAR = lugar
				event_idiom.DESCRIPCION = descripcion
				event_idiom.save(commit)
		return evento


	def clean(self):
		super(EventosChangeForm, self).clean()
		cleaned_data = self.cleaned_data
		latitud = cleaned_data["LATITUD"]
		if latitud !="":
			if re.match(r'([-]?)([0-9]{1,3})[.]([0-9]{1,16})$',latitud) == None:
				self._errors['MAPA']= ErrorList([u"Ocurrió un error interno con el formato de la latitud. Favor de contactar al administrador."])
		longitud = cleaned_data["LONGITUD"]
		if longitud !="":
			if re.match(r'([-]?)([0-9]{1,3})[.]([0-9]{1,16})$',longitud) == None:
				if not self._errors.has_key('MAPA'):
					self._errors['MAPA']= ErrorList([u"Ocurrió un error interno con el formato de la latitud. Favor de contactar al administrador."])
		return cleaned_data

#------------------------------Fin de formularios para el modelo de eventos-------------------

#------------------------------Formularios para el modelo de relatos------------------------

class RelatosForm(forms.ModelForm):
	# ADMINISTRADORES = forms.ModelMultipleChoiceField(label='Administradores ',queryset = User.objects.exclude(username='root'), widget = SelectMultipleCustom())
	FECHA_P = forms.CharField(max_length=20,required=False, widget=HiddenInput())
	exclude = ('FECHA',) 
	class Media:
		#css={'all':('admin/css/multi-select.css',),}
		js=('admin/js/relatos.js',)
	class Meta:
		model=relato
	def __init__(self, *args, **kwargs):
		#El campo username tiene sus propios validadores o metodos para validar el contenido del campo.
		super(RelatosForm, self).__init__(*args, **kwargs)
		self.fields['PUEBLO'].help_text= "Obligatorio. Pueblo donde se llevará acabo el evento."
		self.fields['DESCRIPCION'].help_text= "Obligatorio. Información acerca del evento. No más de 2000 caracteres."
		self.fields['DESCRIPCION'].widget=AccordionMultipleTextbox(attrs = {'rows':'10','class':'vTextField span10','maxlength':'2000'})
		self.fields['TITULO'].help_text= "Obligatorio. Nombre del relato. No más de 30 caracteres."
		self.fields['TITULO'].widget=AccordionMultiplesSimpleTextbox(attrs={'maxlength':'30'})



	def save(self,commit=True):
		# import pdb
		# pdb.set_trace()
		relato = super(RelatosForm, self).save(commit=False)
		if self.data.__contains__('FECHA_P'):
			fecha=self.data['FECHA_P']
			fechaObj=datetime.datetime.strptime(fecha,"%d/%m/%Y %H:%M:%S")
			relato.FECHA=fechaObj
		else:
			relato.FECHA= datetime.datetime.now()
		
		relato.save()
		import pdb
		pdb.set_trace()
		for idioma in IDIOMAS:
			titulo=""
			descripcion=""
			nombre="TITULO_"+idioma[0]
			if self.data.__contains__(nombre):
				titulo=self.data[nombre]
			nombre="DESCRIPCION_"+idioma[0]
			if self.data.__contains__(nombre):
				descripcion=self.data[nombre]
			
			if (titulo != "" or descripcion !=""):
				tit_idiom = relato_idioma()
				tit_idiom.RELATO = relato
				tit_idiom.IDIOMA= idioma[0]
				tit_idiom.TITULO = titulo
				tit_idiom.DESCRIPCION = descripcion
				tit_idiom.save(commit)
		return relato

	def clean(self):
		# import pdb
		# pdb.set_trace()
		super(RelatosForm, self).clean()
		cleaned_data = self.cleaned_data
		return cleaned_data

class RelatosChangeForm(forms.ModelForm):
	FECHA_P = forms.CharField(max_length=20,required=False, widget=HiddenInput())
	class Meta:
		model=relato
	class Media:
		#css={'all':('admin/css/multi-select.css',),}
		js=('admin/js/relatos.js',)
	def __init__(self, *args, **kwargs):
		#El campo username tiene sus propios validadores o metodos para validar el contenido del campo.
		super(RelatosChangeForm, self).__init__(*args, **kwargs)
		self.fields['PUEBLO'].help_text= "Obligatorio. Pueblo donde se llevará acabo el evento."
		
		obj = kwargs['instance']
		titulo = {u'Español' : obj.TITULO}
		descripcion = {u'Español' : obj.DESCRIPCION}
		try:
			relats_idioms=relato_idioma.objects.get(RELATO=obj)

			if isinstance(relats_idioms,relato_idioma):
				titulo[u''+relats_idioms.IDIOMA]=relats_idioms.TITULO
				descripcion[u''+relats_idioms.IDIOMA]=relats_idioms.DESCRIPCION
			elif isinstance(relats_idioms,list):
				for relat_idioms in relats_idioms:
					titulo[event_idioms.IDIOMA]=event_idioms.TITULO
					descripcion[relat_idioms.IDIOMA]=relat_idioms.DESCRIPCION
			
		except  relato_idioma.DoesNotExist, e:
			pass
		self.fields['DESCRIPCION'].help_text= "Obligatorio. Información acerca del evento. No más de 2000 caracteres."
		self.fields['DESCRIPCION'].widget=AccordionMultipleTextbox(attrs = {'rows':'10','class':'vTextField span10','maxlength':'2000'},data=descripcion)
		self.fields['TITULO'].help_text= "Obligatorio. Nombre del relato. No más de 30 caracteres."
		self.fields['TITULO'].widget=AccordionMultiplesSimpleTextbox(attrs={'maxlength':'30'},data=titulo)

	def save(self,commit=True):
		# import pdb
		# pdb.set_trace()
		relato = super(RelatosChangeForm, self).save(commit=False)
		if self.data.__contains__('FECHA_P'):
			fecha=self.data['FECHA_P']
			fechaObj=datetime.datetime.strptime(fecha,"%d/%m/%Y %H:%M:%S")
			relato.FECHA=fechaObj
		else:
			relato.FECHA= datetime.datetime.now()
		
		relato.save()

		for idioma in IDIOMAS:
			
			titulo=""
			descripcion=""
			nombre="TITULO_"+idioma[0]
			if self.data.__contains__(nombre):
				titulo=self.data[nombre]
			nombre="DESCRIPCION_"+idioma[0]
			if self.data.__contains__(nombre):
				descripcion=self.data[nombre]
			
			if (titulo != "" or descripcion !=""):
				tit_idiom = relato_idioma()
				tit_idiom.RELATO = relato
				tit_idiom.IDIOMA= idioma[0]
				tit_idiom.TITULO = titulo
				tit_idiom.DESCRIPCION = descripcion
				tit_idiom.save(commit)
		return relato

	def clean(self):
		# import pdb
		# pdb.set_trace()
		super(RelatosChangeForm, self).clean()
		cleaned_data = self.cleaned_data
		return cleaned_data

#------------------------------Fin de formularios para el modelo de eventos-------------------


#------------------------------Formularios para el modelo de SitiosTuristicos-------------------

class SitiosTuristicosForm(forms.ModelForm):
	LATITUD = forms.CharField(required=False)
	LONGITUD = forms.CharField(required=False)
	MAPA = forms.CharField(required=False)
	class Media:
		#css={'all':('admin/css/multi-select.css',),}
		js=('admin/js/sitiosTuristicos.js',)
	class Meta:
		model=sitio_turistico
	def __init__(self, *args, **kwargs):
		#El campo username tiene sus propios validadores o metodos para validar el contenido del campo.
		super(SitiosTuristicosForm, self).__init__(*args, **kwargs)
		self.fields['NOMBRE'].help_text= "Obligatorio. Nombre del la empresa."
		self.fields['PUEBLO'].help_text= "Obligatorio. Pueblo donde está ubicado la empresa."
		self.fields['DIRECCION'].help_text= "Obligatorio. Lugar donde se encuentra el negocio. No más de 100 caracteres"
		self.fields['CATEGORIA'].help_text= "Obligatorio. Tipo de negocio o giro comercial."
		self.fields['TELEFONOS'].help_text= "Obligatorio. Número o números para poder contactar al local. Ejemplo: Tel: 6121578921;6121789413. Cel: 6121705677. No más de 100 caracteres."
		self.fields['TELEFONOS'].widget.attrs={'rows':'3','class':'vTextField span8','maxlength':'100'}
		self.fields['TELEFONOS'].required=False
		self.fields['PRECIO_DESDE'].help_text= "Opcional. Intervalo incial del servicio propuesto del sitio, en dado caso que así lo preste. La moneda utilizada es el dolar americano."
		self.fields['PRECIO_HASTA'].help_text= "Opcional. Intervalo final del servicio propuesto del sitio, en dado caso que así lo preste. La moneda utilizada es el dolar americano. En dado caso que se coloque uno de ellos es OBLIGATORIO que el inicial sea menor que el final."
		self.fields['URL'].help_text="Direccion URL del sitio, si lo tuviera. Ejemplo: http://example.com"
		self.fields['URL'].label="Sitio Web"
		self.initial['PRECIO_DESDE'] ='0.00'
		self.initial['PRECIO_HASTA'] ='0.00'
		self.fields['PRECIO_DESDE'].required=False
		self.fields['PRECIO_HASTA'].required=False
		self.fields['IMAGEN'].help_text= "Obligatorio. Banner de la empresa."
		self.fields['DESCRIPCION'].widget=AccordionMultipleTextbox()
		self.fields['DESCRIPCION'].help_text= "Obligatorio. Pueblo donde está ubicado la empresa. No más de 2000 caracteres."
		self.fields['DESCRIPCION'].widget=AccordionMultipleTextbox(attrs = {'rows':'10','class':'vTextField span10','maxlength':'2000'})


		self.fields['LATITUD'].widget = HiddenInput()
		self.fields['LONGITUD'].widget = HiddenInput()
		self.fields['MAPA'].widget = MapInput(attrs={'type':'text',"class":"span12 vTextField"})


	def save(self,commit=True):
		# import pdb
		# pdb.set_trace()
		sitio = super(SitiosTuristicosForm, self).save(commit=False)	
		sitio.save()
		for idioma in IDIOMAS:
			descripcion=""
			nombre="DESCRIPCION_"+idioma[0]
			if self.data.__contains__(nombre):
				descripcion=self.data[nombre]
			
			if (descripcion !=""):
				sit_idiom = sitio_turistico_idioma()
				sit_idiom.SITIO = sitio
				sit_idiom.IDIOMA= idioma[0]
				sit_idiom.DESCRIPCION = descripcion
				sit_idiom.save(commit)
		return sitio

	def clean(self):
		# import pdb
		# pdb.set_trace()
		super(SitiosTuristicosForm, self).clean()
		cleaned_data = self.cleaned_data

		latitud = cleaned_data["LATITUD"]
		if latitud !="":
			if re.match(r'([-]?)([0-9]{1,3})[.]([0-9]{1,16})$',latitud) == None:
				self._errors['MAPA']= ErrorList([u"Ocurrió un error interno con el formato de la latitud. Favor de contactar al administrador."])
		longitud = cleaned_data["LONGITUD"]
		if longitud !="":
			if re.match(r'([-]?)([0-9]{1,3})[.]([0-9]{1,16})$',longitud) == None:
				if not self._errors.has_key('MAPA'):
					self._errors['MAPA']= ErrorList([u"Ocurrió un error interno con el formato de la latitud. Favor de contactar al administrador."])
		inicial=cleaned_data['PRECIO_DESDE']
		fin=cleaned_data['PRECIO_HASTA']
		try:
			if (inicial!=0 and fin!=0):
				if inicial>fin:
					if not self._errors.has_key('PRECIO_DESDE'):
						self._errors['PRECIO_DESDE']= ErrorList([u"El valor del precio inicial no puede ser menor al del precio final."])
		except Exception,e:
			if not self._errors.has_key('PRECIO_DESDE'):
				self._errors['PRECIO_DESDE']= ErrorList([u"Error en el formato de los precios."])
			print e
		return cleaned_data

class SitiosTuristicosChangeForm(forms.ModelForm):
	LATITUD = forms.CharField(required=False)
	LONGITUD = forms.CharField(required=False)
	MAPA = forms.CharField(required=False)
	class Meta:
		model=sitio_turistico
	class Media:
		#css={'all':('admin/css/multi-select.css',),}
		js=('admin/js/sitiosTuristicos.js',)
	def __init__(self, *args, **kwargs):
		#El campo username tiene sus propios validadores o metodos para validar el contenido del campo.
		super(SitiosTuristicosChangeForm, self).__init__(*args, **kwargs)

		self.fields['NOMBRE'].help_text= "Obligatorio. Nombre del la empresa."
		self.fields['PUEBLO'].help_text= "Obligatorio. Pueblo donde está ubicado la empresa."
		self.fields['DESCRIPCION'].help_text= "Obligatorio. Pueblo donde está ubicado la empresa."
		self.fields['DIRECCION'].help_text= "Obligatorio. Lugar donde se encuentra el negocio. No más de 100 caracteres"
		self.fields['CATEGORIA'].help_text= "Obligatorio. Tipo de negocio o giro comercial."
		self.fields['TELEFONOS'].help_text= "Obligatorio. Número o números para poder contactar al local. Ejemplo: Tel: 6121578921;6121789413. Cel: 6121705677. No más de 100 caracteres."
		self.fields['TELEFONOS'].widget.attrs={'rows':'3','class':'vTextField span8','maxlength':'100'}
		self.fields['TELEFONOS'].required=False
		self.fields['PRECIO_DESDE'].help_text= "Opcional. Intervalo incial del servicio propuesto del sitio, en dado caso que así lo preste. La moneda utilizada es el dolar americano."
		self.fields['PRECIO_HASTA'].help_text= "Opcional. Intervalo final del servicio propuesto del sitio, en dado caso que así lo preste. La moneda utilizada es el dolar americano. En dado caso que se coloque uno de ellos es OBLIGATORIO que el inicial sea menor que el final."
		self.fields['PRECIO_DESDE'].required=False
		self.fields['PRECIO_HASTA'].required=False
		self.fields['URL'].help_text="Direccion URL del sitio, si lo tuviera. Ejemplo: http://example.com"
		self.fields['URL'].label="Sitio Web"
		self.fields['IMAGEN'].help_text= "Obligatorio. Banner de la empresa."
		self.fields['LATITUD'].widget = HiddenInput()
		self.fields['LONGITUD'].widget = HiddenInput()
		self.fields['MAPA'].widget = MapInput(attrs={'type':'text',"class":"span12 vTextField"})
		self.fields['NOMBRE'].widget.attrs['readonly'] = 'true'

		obj = kwargs['instance']
		descripcion = {u'Español' : obj.DESCRIPCION}
		try:
			sits_idioms=sitio_turistico_idioma.objects.get(SITIO=obj)

			if isinstance(sits_idioms,sitio_turistico_idioma):
				descripcion[u''+sits_idioms.IDIOMA]=sits_idioms.DESCRIPCION
			elif isinstance(sits_idioms,list):
				for sits_idiom in sits_idioms:
					descripcion[sits_idiom.IDIOMA]=sits_idiom.DESCRIPCION
			
		except  sitio_turistico_idioma.DoesNotExist, e:
			pass
		self.fields['DESCRIPCION'].widget=AccordionMultipleTextbox(attrs = {'rows':'10','class':'vTextField span10','maxlength':'2000'},data=descripcion)
		self.fields['DESCRIPCION'].help_text= "Obligatorio. Pueblo donde está ubicado la empresa. No más de 2000 caracteres."

		
		coordenadas= {}
		if (obj.LATITUD is not None and obj.LONGITUD is not None):
			coordenadas['LATITUD'] = obj.LATITUD
			coordenadas['LONGITUD'] = obj.LONGITUD
		else:
			coordenadas['LATITUD'] = ""
			coordenadas['LONGITUD'] = ""
		self.fields['MAPA'].widget = MapInput(attrs={'type':'text',"class":"span12 vTextField"},data=coordenadas)

	def save(self,commit=True):
		# import pdb
		# pdb.set_trace()
		sitio = super(SitiosTuristicosChangeForm, self).save(commit=False)	
		sitio.save()
		for idioma in IDIOMAS:
			descripcion=""
			nombre="DESCRIPCION_"+idioma[0]
			if self.data.__contains__(nombre):
				descripcion=self.data[nombre]
			
			if (titulo != "" or descripcion !=""):
				sit_idiom = sitio_turistico_idioma()
				sit_idiom.SITIO = sitio
				sit_idiom.IDIOMA= idioma[0]
				sit_idiom.DESCRIPCION = descripcion
				sit_idiom.save(commit)
		return sitio

	def clean(self):
		# import pdb
		# pdb.set_trace()
		super(SitiosTuristicosChangeForm, self).clean()
		cleaned_data = self.cleaned_data

		latitud = cleaned_data["LATITUD"]
		if latitud !="":
			if re.match(r'([-]?)([0-9]{1,3})[.]([0-9]{1,16})$',latitud) == None:
				self._errors['MAPA']= ErrorList([u"Ocurrió un error interno con el formato de la latitud. Favor de contactar al administrador."])
		longitud = cleaned_data["LONGITUD"]
		if longitud !="":
			if re.match(r'([-]?)([0-9]{1,3})[.]([0-9]{1,16})$',longitud) == None:
				if not self._errors.has_key('MAPA'):
					self._errors['MAPA']= ErrorList([u"Ocurrió un error interno con el formato de la latitud. Favor de contactar al administrador."])
		inicial=cleaned_data['PRECIO_DESDE']
		fin=cleaned_data['PRECIO_HASTA']
		try:
			if (inicial!=0 and fin!=0):
				if inicial>fin:
					if not self._errors.has_key('PRECIO_DESDE'):
						self._errors['PRECIO_DESDE']= ErrorList([u"El valor del precio inicial no puede ser menor al del precio final."])
		except Exception,e:
			if not self._errors.has_key('PRECIO_DESDE'):
				self._errors['PRECIO_DESDE']= ErrorList([u"Error en el formato de los precios."])
			print e
		return cleaned_data

#------------------------------Fin de formularios para el modelo de SitiosTuristicos------------

#------------------------------Formularios para el modelo de Categorias------------------------

class CategoriasForm(forms.ModelForm):
	class Media:
		#css={'all':('admin/css/multi-select.css',),}
		js=('admin/js/categorias.js',)
	class Meta:
		model=categoria
	def __init__(self, *args, **kwargs):
		#El campo username tiene sus propios validadores o metodos para validar el contenido del campo.
		super(CategoriasForm, self).__init__(*args, **kwargs)
		self.fields['NOMBRE'].help_text= "Obligatorio. Nombre del la categoría. No menor de 4 carácteres y no mayor de 30. Sólo caracteres."

class CategoriasChangeForm(forms.ModelForm):
	class Meta:
		model=categoria
	class Media:
		#css={'all':('admin/css/multi-select.css',),}
		js=('admin/js/categorias.js',)
	def __init__(self, *args, **kwargs):
		#El campo username tiene sus propios validadores o metodos para validar el contenido del campo.
		super(CategoriasChangeForm, self).__init__(*args, **kwargs)
		self.fields['NOMBRE'].help_text= "Obligatorio. Nombre del la categoría. No menor de 4 carácteres y no mayor de 30. Sólo caracteres."

#---------------------------Fin de formularios para el modelo de Categorias-------------------

#------------------------------Formularios para el modelo de Contratos----------------------

class ContratosForm(forms.ModelForm):
	Nombre = forms.CharField(required=False)
	class Media:
		#css={'all':('admin/css/multi-select.css',),}
		js=('admin/js/contratos.js',)
	class Meta:
		model=contrato
	def __init__(self, *args, **kwargs):
		#El campo username tiene sus propios validadores o metodos para validar el contenido del campo.
		super(ContratosForm, self).__init__(*args, **kwargs)
		self.fields['SITIO'].help_text= "Obligatorio. Nombre del la empresa que solicita el contrato de publicidad."
		self.fields['OBSERVACION'].help_text= "Opcional. Notas o datos adicionales del contrato. No más de 30 caracteres"
		self.fields['OBSERVACION'].required=False
		self.fields['FECHA_INICIO'].help_text= "Obligatorio. Fecha desde la cuál se empieza a llevar a cabo la publicidad."
		self.initial['FECHA_INICIO']=datetime.date.today()
		#self.fields['FECHA_INICIO'].widget.attrs['readonly']= 'true'
		self.fields['DURACION'].help_text= "Obligatorio. Tiempo durante el cual estará mostrandose la publicidad. El tiempo esta dado en meses de 30 días."
		choices= [(str(i),i) for i in range(0,11)]
		choices = tuple(choices)
		self.fields['DURACION'].widget = forms.widgets.Select(choices=choices)

class ContratosChangeForm(forms.ModelForm):
	class Meta:
		model=contrato
	class Media:
		#css={'all':('admin/css/multi-select.css',),}
		js=('admin/js/contratos.js',)
	def __init__(self, *args, **kwargs):
		#El campo username tiene sus propios validadores o metodos para validar el contenido del campo.
		super(ContratosChangeForm, self).__init__(*args, **kwargs)

		self.fields['SITIO'].help_text= "Obligatorio. Nombre del la empresa que solicita el contrato de publicidad."
		self.fields['OBSERVACION'].help_text= "Opcional. Notas o datos adicionales del contrato. No más de 30 caracteres"
		self.fields['OBSERVACION'].required=False
		self.fields['FECHA_INICIO'].help_text= "Obligatorio. Fecha desde la cuál se empieza a llevar a cabo la publicidad."
		self.initial['FECHA_INICIO']=datetime.date.today()
		#self.fields['FECHA_INICIO'].widget.attrs['readonly']= 'true'
		self.fields['DURACION'].help_text= "Obligatorio. Tiempo durante el cual estará mostrandose la publicidad. El tiempo esta dado en meses de 30 días."
		choices= [(str(i),i) for i in range(0,11)]
		choices = tuple(choices)
		self.fields['DURACION'].widget = forms.widgets.Select(choices=choices)

#---------------------------Fin de formularios para el modelo de Contratos----------------------

#------------------------------Formularios para el modelo de galerias------------------------

class GaleriasForm(forms.ModelForm):
	usuario = None
	class Media:
		#css={'all':('admin/css/multi-select.css',),}
		js=('admin/js/galerias.js',)
	class Meta:
		model=galeria
	def __init__(self, *args, **kwargs):
		#El campo username tiene sus propios validadores o metodos para validar el contenido del campo.
		super(GaleriasForm, self).__init__(*args, **kwargs)
		self.fields['NOMBRE'].help_text= "Obligatorio. Nombre de la galeria. Sólo caracteres y números y no más de 40."
		self.fields['DESCRIPCION'].help_text= "Opcional. Referencia de la galería. No más de 100 caracteres."
		self.fields['ARCHIVOS'].help_text= "Obligatorio. Listado de archivos a incluir en la galería."
		self.fields['ARCHIVOS'].widget=SelectMultipleCustom()
		self.fields['ARCHIVOS'].queryset=archivo.objects.all()
		self.fields['ARCHIVOS'].widget.attrs = {'class':'input-xxlarge'}
		self.fields['USUARIO'].widget=HiddenInput()
		if self.usuario is not None:
			self.initial['USUARIO']= self.usuario
		else:
			self.initial['USUARIO'] = 'Error'
		#self.fields['FECHA_INICIO'].widget.attrs['readonly']= 'true'

class GaleriasChangeForm(forms.ModelForm):
	usuario = None
	class Meta:
		model=galeria
	class Media:
		#css={'all':('admin/css/multi-select.css',),}
		js=('admin/js/galerias.js',)
	def __init__(self, *args, **kwargs):
		#El campo username tiene sus propios validadores o metodos para validar el contenido del campo.
		super(GaleriasChangeForm, self).__init__(*args, **kwargs)

		self.fields['NOMBRE'].help_text= "Obligatorio. Nombre de la galeria. Sólo caracteres y números y no más de 40."
		self.fields['DESCRIPCION'].help_text= "Opcional. Referencia de la galería. No más de 100 caracteres."
		self.fields['ARCHIVOS'].help_text= "Obligatorio. Listado de archivos a incluir en la galería."
		self.fields['ARCHIVOS'].widget=SelectMultipleCustom()
		self.fields['ARCHIVOS'].queryset=archivo.objects.all()
		self.fields['ARCHIVOS'].widget.attrs = {'class':'input-xxlarge'}
		self.fields['USUARIO'].widget=HiddenInput()
		if self.usuario is not None:
			self.initial['USUARIO']= self.usuario
		else:
			self.initial['USUARIO'] = 'Error'

#---------------------------Fin de formularios para el modelo de galerias----------------------


#------------------------------Formularios para el modelo de archivos------------------------

class ArchivosForm(forms.ModelForm):
	class Media:
		#css={'all':('admin/css/multi-select.css',),}
		js=('admin/js/archivos.js',)
	class Meta:
		model=archivo
	def __init__(self, *args, **kwargs):
		#El campo username tiene sus propios validadores o metodos para validar el contenido del campo.
		super(ArchivosForm, self).__init__(*args, **kwargs)
		self.fields['NOMBRE'].help_text= "Obligatorio. Nombre de la galeria. Sólo caracteres."
		self.fields['NOMBRE'].widget=HiddenInput()
		self.fields['DESCRIPCION'].help_text= "Opcional. Referencia de la galería. No más de 100 caracteres"
		self.fields['RUTA'].help_text= "Obligatorio. Es el archivo que se subirá al servidor. El tamaño del nombre no puede ser mayor de 50 caracteres, y eso incluye la extensión."
		#self.fields['FECHA_INICIO'].widget.attrs['readonly']= 'true'
	def clean(self):
		# import pdb
		# pdb.set_trace()
		super(ArchivosForm, self).clean()

		nombre=self.data['NOMBRE']
		if archivo.objects.filter(NOMBRE=nombre).exists():
			self._errors['RUTA']= ErrorList([u"Ya existe un archivo con un nombre igual al que está tratando de subir."])	

		cleaned_data = self.cleaned_data
		return cleaned_data


class ArchivosChangeForm(forms.ModelForm):
	usuario = None
	class Meta:
		model=archivo
	class Media:
		#css={'all':('admin/css/multi-select.css',),}
		js=('admin/js/archivos.js',)
	def __init__(self, *args, **kwargs):
		#El campo username tiene sus propios validadores o metodos para validar el contenido del campo.
		super(ArchivosChangeForm, self).__init__(*args, **kwargs)

		self.fields['NOMBRE'].help_text= "Obligatorio. Nombre de la galeria. Sólo caracteres."
		self.fields['NOMBRE'].widget=HiddenInput()
		self.fields['DESCRIPCION'].help_text= "Opcional. Referencia de la galería."
		self.fields['RUTA'].help_text= "Obligatorio. Es el archivo que se subirá al servidor. El tamaño del nombre no puede ser mayor de 50 caracteres, y eso incluye la extensión."
		obj = kwargs['instance']
		try:
			self.initial['NOMBRE'] = obj.NOMBRE
		except Exception,e:
			print e

	def clean(self):
		# import pdb
		# pdb.set_trace()
		super(ArchivosChangeForm, self).clean()

		nombre=self.data['NOMBRE']
		cont = archivo.objects.filter(NOMBRE=nombre).count()
		if cont > 0:
			dupl=archivo.objects.filter(NOMBRE=nombre)[0]
			if self.instance.ID!=dupl.ID:
				self._errors['RUTA']= ErrorList([u"Ya existe un archivo con un nombre igual al que está tratando de subir."])

		cleaned_data = self.cleaned_data
		return cleaned_data
#---------------------------Fin de formularios para el modelo de archivos----------------------

#------------------------------Formularios para el modelo de reportes------------------------


class ReporteChangeForm(forms.ModelForm):
	COMENTARIO_REP = forms.CharField(required=False)
	class Meta:
		model=reporte_comentario
	class Media:
		#css={'all':('admin/css/multi-select.css',),}
		js=('admin/js/reportes.js',)
	def __init__(self, *args, **kwargs):
		#El campo username tiene sus propios validadores o metodos para validar el contenido del campo.
		super(ReporteChangeForm, self).__init__(*args, **kwargs)

		self.fields['USUARIO'].widget=TextInput()
		self.fields['USUARIO'].widget.attrs['readonly'] = True
		self.fields['CLASE_COMENTARIO'].widget= HiddenInput()
		self.fields['COMENTARIO'].widget= HiddenInput()
		self.fields['RAZON'].widget.attrs['rows']='2'
		self.fields['RAZON'].widget.attrs['readonly'] = True
		self.fields['FECHA'].widget.attrs['readonly'] = True
		self.fields['USUARIO'].widget.attrs['readonly'] = True
		
		obj = kwargs['instance']

		self.fields['COMENTARIO_REP'].widget = VerInput(data={'tipo_comentario':obj.CLASE_COMENTARIO,'id':obj.COMENTARIO})
		self.fields['COMENTARIO_REP'].label='Comentario'
		self.fields['COMENTARIO_REP'].widget.attrs['readonly'] = True
		self.fields['COMENTARIO_REP'].widget.attrs['rows']='2'

		self.initial['USUARIO'] = obj.USUARIO.username
		try:
			if obj.CLASE_COMENTARIO=='R':
				comen=comentario_relato.objects.get(ID=obj.COMENTARIO)
				self.initial['COMENTARIO_REP'] = comen.DESCRIPCION
			elif obj.CLASE_COMENTARIO=='E':
				comen=comentario_evento.objects.get(ID=obj.COMENTARIO)
				self.initial['COMENTARIO_REP'] = comen.DESCRIPCION
			elif obj.CLASE_COMENTARIO=='S':
				comen=comentario_sitio.objects.get(ID=obj.COMENTARIO)
				self.initial['COMENTARIO_REP'] = comen.DESCRIPCION
			elif obj.CLASE_COMENTARIO=='P':
				comen=comentario_pueblo.objects.get(ID=obj.COMENTARIO)
				self.initial['COMENTARIO_REP'] = comen.DESCRIPCION
		except Exception, e:
			print e

	def clean(self):
		# import pdb
		# pdb.set_trace()
		super(ReporteChangeForm, self).clean()
		cleaned_data = self.cleaned_data
		return cleaned_data
#---------------------------Fin de formularios para el modelo de reportes----------------------




