#admin.py
# -*- encoding: utf-8 -*-
from django.contrib import admin
from administrador.models import *
from principal.models import *
from administrador.formas import *
from django.contrib.auth.models import User,Group

admin.site.login_form = CustomAutenticacionForm

# #print admin.site.get_urls()

#ModelAdmin de Idiomas para el manejo de las paginas para agregar, modificar y mostrar elementos
class IdiomasAdmin(admin.ModelAdmin):
	class Media:
		js = ('admin/js/idiomas.js',) #No preocuparse por agregar la referencia "static" al directorio.
		css = {}
	list_per_page = 5
	search_fields = ('NOMBRE',)
	ordering = ['NOMBRE',]

#ModelAdmin de Usuarios para el manejo de las paginas para agregar, modificar y mostrar elementos
class UsuarioAdmin(admin.ModelAdmin):
	list_display =('username','first_name','last_name','email','is_staff',)
	search_fields = ['username',]
	list_per_page = 10
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
					'fields': ('is_active','is_superuser','is_staff','groups','user_permissions',)
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
					'fields': ('is_active','is_superuser','is_staff','groups','user_permissions',)
					}),
				)
		return super(UsuarioAdmin, self).get_form(request, obj, **kwargs)	
        # def __init__(self, *args, **kwargs):
        #     super(UsuarioAdmin, self).__init__(*args, **kwargs)
#Fin del UsuarioAdmin

#ModelAdmin de Grupos para el manejo de las paginas para agregar, modificar y mostrar elementos
class GruposAdmin(admin.ModelAdmin):
	list_display =('name',)
	list_per_page = 10
	def get_form(self, request, obj=None, **kwargs):
		#print dir(self.form._meta.fields)
		if obj: # obj is not None, so this is a change page
			pass
			#kwargs['fields'] = ['username', 'password','password2']
			self.form=GroupChangeForm
			self.fieldsets = (
				(None, {
					'fields': ('name','permissions'),
					}),
				)
		else: # obj is None, so this is an add page
			self.form=GroupForm
			self.fieldsets = (
				(None, {
					'fields': ('name','permissions'),
					}),
				)
		return super(GruposAdmin, self).get_form(request, obj, **kwargs)	
#Fin del UsuarioAdmin

#ModelAdmin de Pueblos para el manejo de las paginas para agregar, modificar y mostrar elementos
class PueblosAdmin(admin.ModelAdmin):
	list_display =('NOMBRE','TIPO')
	list_per_page = 10
	list_filter = ('TIPO',)
	search_fields = ['NOMBRE',]
	def get_form(self, request, obj=None, **kwargs):
		#print dir(self.form._meta.fields)
		if obj: # obj is not None, so this is a change page
			pass
			#kwargs['fields'] = ['username', 'password','password2']
			self.form=PuebloChangeForm
			self.fieldsets = (
				(None, {
					'fields': ('NOMBRE','TIPO','DESCRIPCION','MAPA','LATITUD','LONGITUD',),
					}),
				)
		else: # obj is None, so this is an add page
			self.form=PuebloForm
			# self.fieldsets = (
			# 	(None, {
			# 		'fields': ('name','permissions'),
			# 		}),
			# 	)
		return super(PueblosAdmin, self).get_form(request, obj, **kwargs)	
#Fin del UsuarioAdmin


admin.site.unregister(User)
admin.site.register(User,UsuarioAdmin)
admin.site.unregister(Group)
admin.site.register(Group,GruposAdmin)
admin.site.register(idioma,IdiomasAdmin)
admin.site.register(pueblo,PueblosAdmin)

# admin.site.register(idioma)
# admin.site.register(pueblo)

admin.site.register(archivo)
admin.site.register(galeria)
admin.site.register(pueblo_idioma)
admin.site.register(pueblo_administrador)
admin.site.register(comentario_pueblo)
admin.site.register(evento)
admin.site.register(evento_idioma)
admin.site.register(comentario_evento)
admin.site.register(relato)
admin.site.register(relato_idioma)
admin.site.register(comentario_relato)
admin.site.register(categoria)
admin.site.register(sitio_turistico)
admin.site.register(sitio_turistico_idioma)
admin.site.register(comentario_sitio)
admin.site.register(contrato)
admin.site.register(reporte_comentario)
admin.site.register(curiosidad_idioma)
admin.site.register(curiosidad)