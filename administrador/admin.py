#admin.py
# -*- encoding: utf-8 -*-
from django.contrib import admin
from administrador.models import *
from principal.models import *
from administrador.formas import *
from django.contrib.auth.models import User

# from django.contrib.auth.models import User
# from django.contrib.auth.admin import *

# class PersonaAdmin(admin.ModelAdmin):
#     list_display = ('NOMBRE', 'DIRECCION','SEXO','TELEFONO','EMAIL',)
#     list_filter = ('SEXO',)   
#     list_per_page = 5
#     ordering = ['NOMBRE',]
#     search_fields = ['EMAIL',]

# class CasaAdmin(admin.ModelAdmin):
#     actions_on_top=False
#     actions_on_bottom=True
#     list_display = ('NUMERO','ANCHO','LARGO','AREA')
#     list_per_page = 5

# admin.site.register(Persona,PersonaAdmin)
# admin.site.register(Casa,CasaAdmin)

# class ArchivoAdmin(admin.ModelAdmin):
# 	list_display = ('NOMBRE', 'DESCRIPCION', 'TIPO',) #Para desplegar los campos que se quieran en el gestor
# 	search_fields = ('NOMBRE',) #Campos a considerar en las busquedas
# 	list_filter= ('TIPO',) #Campos a utilizar como filtros
# 	ordering = ('NOMBRE',)

# class GaleriaAdmin(admin.ModelAdmin):
# 	filter_horizontal = ('ARCHIVOS',)
# 	raw_id_fields = ('USUARIO',)

class IdiomaAdmin(admin.ModelAdmin):
	class Media:
		js = ('admin/js/idiomas.js',) #No preocuparse por agregar la referencia "static" al directorio.
		css = {}
	list_per_page = 5
	search_fields = ('NOMBRE',)
	ordering = ['NOMBRE',]

class UsuarioAdmin(admin.ModelAdmin):
	list_display =('username','first_name','last_name','email','is_staff',)
	def get_form(self, request, obj=None, **kwargs):
		#print dir(self.form._meta.fields)
		if obj: # obj is not None, so this is a change page
			pass
			#kwargs['fields'] = ['username', 'password','password2']
			self.form=UserChangeForm
			self.fieldsets = (
				(None, {
					'fields': ('username',)
					}),
				('Datos personales', {
					'fields': ('first_name', 'last_name', 'email',)
					}),
				('Privilegios del usuario', {
					'fields': ('is_active','is_staff','groups','user_permissions',)
					}),
				)
		else: # obj is None, so this is an add page
			self.form=UserForm
			self.fieldsets = (
				(None, {
					'fields': ('username', 'password','password2')
					}),
				('Datos personales', {
					'classes': ('collapse',),
					'fields': ('first_name', 'last_name', 'email',)
					}),
				('Privilegios del usuario', {
					'classes': ('collapse',),
					'fields': ('is_active','is_staff','groups','user_permissions',)
					}),
				)
		return super(UsuarioAdmin, self).get_form(request, obj, **kwargs)	
        # def __init__(self, *args, **kwargs):
        #     super(UsuarioAdmin, self).__init__(*args, **kwargs)


    #id_groups,id_user_permissions,id_last_login_0,id_date_joined_0
admin.site.unregister(User)
admin.site.register(User,UsuarioAdmin)

admin.site.register(idioma,IdiomaAdmin)


# admin.site.register(archivo,ArchivoAdmin)
# admin.site.register(galeria,GaleriaAdmin)
# admin.site.register(pueblo)
# admin.site.register(pueblo_idioma)
# admin.site.register(pueblo_administrador)
# admin.site.register(comentario_pueblo)
# admin.site.register(evento)
# admin.site.register(evento_idioma)
# admin.site.register(comentario_evento)
# admin.site.register(relato)
# admin.site.register(relato_idioma)
# admin.site.register(comentario_relato)
# admin.site.register(categoria)
# admin.site.register(sitio_turistico)
# admin.site.register(sitio_turistico_idioma)
# admin.site.register(comentario_sitio)
# admin.site.register(contrato)
# admin.site.register(reporte_comentario)
# admin.site.register(curiosidad_idioma)
# admin.site.register(curiosidad)






# class MyForm(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         super(MyForm, self).__init__(*args, **kwargs)
#         self.fields['myfield'].help_text = 'New help text!'


# class PropertyForm(models.ModelAdmin):
#     class Meta:
#         model = Property
#     def __init__(self, *args, **kwargs):
#         super(PropertyForm, self).__init__(*args, **kwargs)
#         for (key, val) in self.fields.iteritems():
#             self.fields[key].help_text = 'what_u_want' 