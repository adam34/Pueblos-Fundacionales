#admin.py
# -*- encoding: utf-8 -*-
from django.contrib import admin
from administrador.models import *
from principal.models import *
from administrador.formas import *
from django.contrib.auth.models import User,Group

admin.site.login_form = CustomAutenticacionForm

# #print admin.site.get_urls()

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
	list_display =('NOMBRE','TIPO','ADMINISTRADOR',)
	list_per_page = 10
	list_filter = ('TIPO','ADMINISTRADOR',)
	search_fields = ['NOMBRE',]
	ordering = ['NOMBRE']
	def get_form(self, request, obj=None, **kwargs):
		#print dir(self.form._meta.fields)
		if obj: # obj is not None, so this is a change page
			pass
			self.form=PuebloChangeForm
			self.fieldsets = (
				(None, {
					'fields': ('NOMBRE','TIPO','GALERIA','ADMINISTRADOR','MUNICIPIO','LATITUD','LONGITUD',),
					}),
				('Historia', {
					'classes': ('collapse',),
					'fields': ('HISTORIA',)
					}),
				('Cultura', {
					'classes': ('collapse',),
					'fields': ('CULTURA',)
					}),
				('Comida', {
					'classes': ('collapse',),
					'fields': ('COMIDA',)
					}),
				('Datos', {
					'classes': ('collapse',),
					'fields': ('DATOS',)
					}),
				('Mapa', {
					'classes': ('collapse',),
					'fields': ('MAPA',)
					}),
				)
		else: # obj is None, so this is an add page
			self.form=PuebloForm
			self.fieldsets = (
				(None, {
					'fields': ('NOMBRE','TIPO','GALERIA','ADMINISTRADOR','MUNICIPIO','LATITUD','LONGITUD',),
					}),
				('Historia', {
					'classes': ('collapse',),
					'fields': ('HISTORIA',)
					}),
				('Cultura', {
					'classes': ('collapse',),
					'fields': ('CULTURA',)
					}),
				('Comida', {
					'classes': ('collapse',),
					'fields': ('COMIDA',)
					}),
				('Datos', {
					'classes': ('collapse',),
					'fields': ('DATOS',)
					}),
				('Mapa', {
					'classes': ('collapse',),
					'fields': ('MAPA',)
					}),
				)
		return super(PueblosAdmin, self).get_form(request, obj, **kwargs)
	def change_view(self, request, object_id, form_url='', extra_context=None):
		# import pdb
		# pdb.set_trace()
		# algo=0
		return super(PueblosAdmin, self).change_view(request, object_id,form_url,extra_context)
	def add_view(self, request, form_url='', extra_context=None):
		# import pdb
		# pdb.set_trace()
		# algo=0
		return super(PueblosAdmin, self).add_view(request, form_url,extra_context)

#Fin del PueblosAdmin

#ModelAdmin de Curiosidades para el manejo de las paginas para agregar, modificar y mostrar elementos
class CuriosidadesAdmin(admin.ModelAdmin):
	list_display =('TITULO','PUEBLO')
	list_per_page = 10
	search_fields = ['NOMBRE',]
	def get_form(self, request, obj=None, **kwargs):
		#print dir(self.form._meta.fields)
		if obj: # obj is not None, so this is a change page
			pass
			#kwargs['fields'] = ['username', 'password','password2']
			self.form=CuriosidadesChangeForm
			self.fieldsets = (
				(None, {
					'fields': ('PUEBLO','TITULO','DESCRIPCION',),
					}),
				)
		else: # obj is None, so this is an add page
			self.form=CuriosidadesForm
			self.fieldsets = (
				(None, {
					'fields': ('PUEBLO','TITULO','DESCRIPCION',),
					}),
				)
		return super(CuriosidadesAdmin, self).get_form(request, obj, **kwargs)	
#Fin del CuriosidadesAdmin

#ModelAdmin de eventos para el manejo de las paginas para agregar, modificar y mostrar elementos
class EventosAdmin(admin.ModelAdmin):
	list_display =('NOMBRE','FECHA',)
	list_per_page = 10
	search_fields = ['NOMBRE',]
	def get_form(self, request, obj=None, **kwargs):
		#print dir(self.form._meta.fields)
		if obj: # obj is not None, so this is a change page
			pass
			#kwargs['fields'] = ['username', 'password','password2']
			self.form=EventosChangeForm
			self.fieldsets = (
				(None, {
					'fields': ('NOMBRE','PUEBLO','FECHA','IMAGEN','LATITUD','LONGITUD'),
					}),
				('Descripción', {
					'classes': ('collapse',),
					'fields': ('DESCRIPCION',)
					}),
				('Lugar', {
					'classes': ('collapse',),
					'fields': ('LUGAR',)
					}),
				('Mapa', {
					'classes': ('collapse',),
					'fields': ('MAPA',)
					}),
				)
		else: # obj is None, so this is an add page
			self.form=EventosForm
			self.fieldsets = (
				(None, {
					'fields': ('NOMBRE','PUEBLO','FECHA','IMAGEN','LATITUD','LONGITUD'),
					}),
				('Descripción', {
					'fields': ('DESCRIPCION',)
					}),
				('Lugar', {
					'fields': ('LUGAR',)
					}),
				('Mapa', {
					'classes': ('collapse',),
					'fields': ('MAPA',)
					}),
				)
		return super(EventosAdmin, self).get_form(request, obj, **kwargs)	
#Fin del EventosAdmin

#ModelAdmin de relatos para el manejo de las paginas para agregar, modificar y mostrar elementos
class RelatosAdmin(admin.ModelAdmin):
	list_display =('TITULO','USUARIO','APROBADO')
	list_per_page = 10
	search_fields = ['TITULO','USUARIO']
	list_filter = ('USUARIO','APROBADO',)
	def get_form(self, request, obj=None, **kwargs):
		#print dir(self.form._meta.fields)
		if obj: # obj is not None, so this is a change page
			pass
			#kwargs['fields'] = ['username', 'password','password2']
			self.form=RelatosChangeForm
			self.fieldsets = (
				(None, {
					'fields': ('USUARIO','PUEBLO','FECHA_P',),
					}),
				('Titulo', {
					'fields': ('TITULO',)
					}),
				('Descripción', {
					'fields': ('DESCRIPCION',)
					}),
				(None, {
					'fields': ('APROBADO',)
					}),
				)
		else: # obj is None, so this is an add page
			self.form=RelatosForm
			self.fieldsets = (
				(None, {
					'fields': ('USUARIO','PUEBLO','FECHA_P',),
					}),
				('Titulo', {
					'fields': ('TITULO',)
					}),
				('Descripción', {
					'fields': ('DESCRIPCION',)
					}),
				(None, {
					'fields': ('APROBADO',)
					}),
				)
		return super(RelatosAdmin, self).get_form(request, obj, **kwargs)	
#Fin del RelatosAdmin

#ModelAdmin de SitiosTuristicos para el manejo de las paginas para agregar, modificar y mostrar elementos
class SitiosTuristicosAdmin(admin.ModelAdmin):
	list_display =('NOMBRE',)
	list_per_page = 10
	search_fields = ['NOMBRE',]
	def get_form(self, request, obj=None, **kwargs):
		#print dir(self.form._meta.fields)
		if obj: # obj is not None, so this is a change page
			pass
			#kwargs['fields'] = ['username', 'password','password2']
			self.form=SitiosTuristicosChangeForm
			self.fieldsets = (
				(None, {
					'fields': ('NOMBRE','PUEBLO','DESCRIPCION','DIRECCION','CATEGORIA','TELEFONOS','PRECIO_DESDE','PRECIO_HASTA','IMAGEN','URL','MAPA','LATITUD','LONGITUD',),
					}),
				)
		else: # obj is None, so this is an add page
			self.form=SitiosTuristicosForm
			self.fieldsets = (
				(None, {
					'fields': ('NOMBRE','PUEBLO','DESCRIPCION','DIRECCION','CATEGORIA','TELEFONOS','PRECIO_DESDE','PRECIO_HASTA','IMAGEN','URL','MAPA','LATITUD','LONGITUD',),
					}),
				)
		return super(SitiosTuristicosAdmin, self).get_form(request, obj, **kwargs)	
#Fin del SitiosTuristicosAdmin


#ModelAdmin de Categorias para el manejo de las paginas para agregar, modificar y mostrar elementos
class CategoriasAdmin(admin.ModelAdmin):
	list_display =('NOMBRE',)
	list_per_page = 10
	search_fields = ['NOMBRE',]
	ordering = ['NOMBRE',]
	def get_form(self, request, obj=None, **kwargs):
		#print dir(self.form._meta.fields)
		if obj: # obj is not None, so this is a change page
			pass
			#kwargs['fields'] = ['username', 'password','password2']
			self.form=CategoriasChangeForm
		else: # obj is None, so this is an add page
			self.form=CategoriasForm
		return super(CategoriasAdmin, self).get_form(request, obj, **kwargs)
#Fin del Categorias

#ModelAdmin de Contratos para el manejo de las paginas para agregar, modificar y mostrar elementos
class ContratosAdmin(admin.ModelAdmin):
	list_display =('SITIO','FECHA_INICIO','DURACION')
	list_per_page = 10
	search_fields = ['SITIO',]
	def get_form(self, request, obj=None, **kwargs):
		#print dir(self.form._meta.fields)
		if obj: # obj is not None, so this is a change page
			pass
			#kwargs['fields'] = ['username', 'password','password2']
			self.form=ContratosChangeForm
			self.fieldsets = (
				(None, {
					'fields': ('SITIO','OBSERVACION','FECHA_INICIO','DURACION',),
					}),
				)
		else: # obj is None, so this is an add page
			self.form=ContratosForm
			self.fieldsets = (
				(None, {
					'fields': ('SITIO','OBSERVACION','FECHA_INICIO','DURACION',),
					}),
				)
		return super(ContratosAdmin, self).get_form(request, obj, **kwargs)
	# def __init__(self, *args, **kwargs):
	# 	super(ContratosAdmin, self).__init__(*args, **kwargs)
#Fin del ContratosAdmin

#ModelAdmin de Categorias para el manejo de las paginas para agregar, modificar y mostrar elementos
class IdiomasAdmin(admin.ModelAdmin):
	list_display =('NOMBRE',)
	list_per_page = 10
	search_fields = ['NOMBRE',]
	def get_form(self, request, obj=None, **kwargs):
		#print dir(self.form._meta.fields)
		if obj: # obj is not None, so this is a change page
			pass
			#kwargs['fields'] = ['username', 'password','password2']
			self.form=IdiomasChangeForm
		else: # obj is None, so this is an add page
			self.form=IdiomasForm
		return super(IdiomasAdmin, self).get_form(request, obj, **kwargs)
#Fin del Categorias

#ModelAdmin de Contratos para el manejo de las paginas para agregar, modificar y mostrar elementos
class GaleriasAdmin(admin.ModelAdmin):
	list_display =('NOMBRE',)
	list_per_page = 10
	search_fields = ['NOMBRE',]
	def get_form(self, request, obj=None, **kwargs):
		#print dir(self.form._meta.fields)
		if obj: # obj is not None, so this is a change page
			pass
			#kwargs['fields'] = ['username', 'password','password2']
			self.form=GaleriasChangeForm
			self.form.usuario=request.user.id
			self.fieldsets = (
				(None, {
					'fields': ('NOMBRE','DESCRIPCION','ARCHIVOS','USUARIO'),
					}),
				)
		else: # obj is None, so this is an add page
			self.form=GaleriasForm
			self.form.usuario=request.user.id
			self.fieldsets = (
				(None, {
					'fields': ('NOMBRE','DESCRIPCION','ARCHIVOS','USUARIO'),
					}),
				)
		return super(GaleriasAdmin, self).get_form(request, obj, **kwargs)
	# def __init__(self, *args, **kwargs):
	# 	super(ContratosAdmin, self).__init__(*args, **kwargs)
#Fin del ContratosAdmin



#ArchivosAdmin
class ArchivosAdmin(admin.ModelAdmin):
	list_display =('NOMBRE','DESCRIPCION','RUTA')
	list_per_page = 10
	search_fields = ['NOMBRE',]
	def get_form(self, request, obj=None, **kwargs):
		#print dir(self.form._meta.fields)
		if obj: # obj is not None, so this is a change page
			pass
			#kwargs['fields'] = ['username', 'password','password2']
			self.form=ArchivosChangeForm
			self.fieldsets = (
				(None, {
					'fields': ('DESCRIPCION','RUTA','NOMBRE'),
					}),
				)
		else: # obj is None, so this is an add page
			self.form=ArchivosForm
			self.fieldsets = (
				(None, {
					'fields': ('DESCRIPCION','RUTA','NOMBRE'),
					}),
				)
		return super(ArchivosAdmin, self).get_form(request, obj, **kwargs)
	
#Fin ArchivosAdmin

#ModelAdmin de reportes para el manejo de las paginas para agregar, modificar y mostrar elementos
class Reportes_Admin(admin.ModelAdmin):
	list_display =('USUARIO','FECHA')
	list_per_page = 10
	def get_form(self, request, obj=None, **kwargs):
		#print dir(self.form._meta.fields)
		if obj: # obj is not None, so this is a change page
			pass
			#kwargs['fields'] = ['username', 'password','password2']
			self.form=ReporteChangeForm
			self.fieldsets = (
				(None, {
					'fields': ('USUARIO','RAZON','FECHA','COMENTARIO_REP','CLASE_COMENTARIO','COMENTARIO',),
					}),
				)
		return super(Reportes_Admin, self).get_form(request, obj, **kwargs)
	# def __init__(self, *args, **kwargs):
	# 	super(ContratosAdmin, self).__init__(*args, **kwargs)
#Fin del reportes



class Comen_Sitios_Admin(admin.ModelAdmin):
	list_display =('USUARIO','SITIOS','FECHA','DESCRIPCION')
	list_per_page = 10
	search_fields = ['USUARIO','SITIOS',]
	def delete_model(self, request, obj):
		# import pdb
		# pdb.set_trace()
		reportes = reporte_comentario.objects.filter(COMENTARIO=obj.ID)
		for reporte in reportes:
			reporte.delete()

	def delete_model(self, request, obj):
		# import pdb
		# pdb.set_trace()
		reportes = reporte_comentario.objects.filter(COMENTARIO=obj.ID,CLASE_COMENTARIO='S')
		for reporte in reportes:
			reporte.delete()

class Comen_Relatos_Admin(admin.ModelAdmin):
	list_display =('USUARIO','RELATOS','FECHA','DESCRIPCION')
	list_per_page = 10
	search_fields = ['USUARIO','RELATOS',]
	def delete_model(self, request, obj):
		# import pdb
		# pdb.set_trace()
		reportes = reporte_comentario.objects.filter(COMENTARIO=obj.ID,CLASE_COMENTARIO='R')
		for reporte in reportes:
			reporte.delete()


class Comen_Evento_Admin(admin.ModelAdmin):
	list_display =('USUARIO','EVENTO','FECHA','DESCRIPCION')
	list_per_page = 10
	search_fields = ['USUARIO','EVENTO',]
	def delete_model(self, request, obj):
		# import pdb
		# pdb.set_trace()
		reportes = reporte_comentario.objects.filter(COMENTARIO=obj.ID,CLASE_COMENTARIO='E')
		for reporte in reportes:
			reporte.delete()


# admin.site.register(idioma)
# admin.site.register(pueblo)
# admin.site.register(archivo)
# admin.site.register(curiosidad)
# admin.site.register(evento)
#admin.site.register(relato)
#admin.site.register(sitio_turistico)
#admin.site.register(categoria)
#admin.site.register(contrato)
#admin.site.register(galeria)

admin.site.unregister(User)
admin.site.register(User,UsuarioAdmin)
admin.site.unregister(Group)
admin.site.register(Group,GruposAdmin)

admin.site.register(idioma,IdiomasAdmin)
admin.site.register(pueblo,PueblosAdmin)
admin.site.register(curiosidad,CuriosidadesAdmin)
admin.site.register(evento,EventosAdmin)
admin.site.register(relato,RelatosAdmin)
admin.site.register(sitio_turistico,SitiosTuristicosAdmin)
admin.site.register(categoria,CategoriasAdmin)
admin.site.register(contrato,ContratosAdmin)
admin.site.register(galeria,GaleriasAdmin)
admin.site.register(archivo,ArchivosAdmin)
admin.site.register(login)
admin.site.register(reporte_comentario,Reportes_Admin)

admin.site.register(comentario_pueblo)
admin.site.register(comentario_evento,Comen_Evento_Admin)
admin.site.register(comentario_relato,Comen_Relatos_Admin)
admin.site.register(comentario_sitio,Comen_Sitios_Admin)