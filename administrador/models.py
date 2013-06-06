# -*- encoding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.

IDIOMAS =(
	('Ingles',u'Inglés'),
	)

class archivo(models.Model):
	class Meta:
		verbose_name="archivo" #Nombre en singular del modelo
		verbose_name_plural="archivos" #Nombre en plural del modelo
	ID=models.AutoField(primary_key=True)
	NOMBRE=models.CharField(unique=True,max_length=20,null=False)
	DESCRIPCION=models.CharField(max_length=100,null=False, blank=True)
	RUTA=models.ImageField(upload_to='galerias/')
	def __unicode__(self):
		return self.NOMBRE

class galeria(models.Model):
	class Meta:
		verbose_name="galería" #Nombre en singular del modelo
		verbose_name_plural="galerías" #Nombre en plural del modelo
	ID=models.AutoField(primary_key=True)
	NOMBRE=models.CharField(unique=True,max_length=40,null=False)
	DESCRIPCION=models.CharField(max_length=100,null=False)
	USUARIO=models.ForeignKey(User,null=False)
	ARCHIVOS=models.ManyToManyField(archivo)
	def __unicode__(self):
		return self.NOMBRE

#max_digits=5, decimal_places=2
class pueblo(models.Model):
	TIPOS_PUEBLOS=(
		('F','Fundacional'),
		('T','Turístico'),
	)
	MUNICIPIOS =(
		('Mulege','Mulegé'),
		('Comondu','Comondú'),
		('Loreto','Loreto'),
	)
	class Meta:
		verbose_name="pueblo" #Nombre en singular del modelo
		verbose_name_plural="pueblos" #Nombre en plural del modelo
	ID=models.AutoField(primary_key=True)
	NOMBRE=models.CharField(unique=True, max_length=30,null=False)
	ADMINISTRADOR = models.ForeignKey(User,unique=True,null=False)
	MUNICIPIO=models.CharField(max_length=10,null=False,choices=MUNICIPIOS)
	HISTORIA = models.TextField(null=False)
	CULTURA = models.TextField(null=False)
	COMIDA = models.TextField(null=False)
	DATOS =models.TextField(null=False)
	GALERIA = models.ForeignKey('galeria',null=False)
	TIPO=models.CharField(max_length=1,null=False,choices=TIPOS_PUEBLOS)
	LATITUD=models.CharField(max_length=20,null=False)
	LONGITUD=models.CharField(max_length=20,null=False)
	VISITAS=models.PositiveIntegerField(null=False,default=0,blank=True)
	def __unicode__(self):
		return self.NOMBRE
	def get_pueblo_idioma(self,language):
		if language != settings.SELECTED_LANGUAGE:
			cont_pueblos=pueblo_idioma.objects.filter(IDIOMA=language,PUEBLO=self).count()
			if cont_pueblos > 0:
				try:
					obj=pueblo_idioma.objects.get(IDIOMA=language,PUEBLO=self)
					self.HISTORIA=obj.HISTORIA
					self.CULTURA=obj.CULTURA
					self.COMIDA=obj.COMIDA
					self.DATOS=obj.DATOS
				except Exception,e:
					print e
		return self


class pueblo_idioma(models.Model):
	class Meta:
		verbose_name="pueblo_idioma" #Nombre en singular del modelo
		verbose_name_plural="pueblos_idiomas" #Nombre en plural del modelo
	ID=models.AutoField(primary_key=True)
	PUEBLO=models.ForeignKey('Pueblo',null=False)
	IDIOMA=models.CharField(max_length=15, null=False,blank=False,choices=IDIOMAS)
	HISTORIA = models.TextField(null=False)
	CULTURA = models.TextField(null=False)
	COMIDA = models.TextField(null=False)
	DATOS =models.TextField(null=False)
	def __unicode__(self):
		return self.PUEBLO.NOMBRE

class comentario_pueblo(models.Model):
	class Meta:
		verbose_name="comentario de pueblo" #Nombre en singular del modelo
		verbose_name_plural="comentarios de pueblos" #Nombre en plural del modelo
	ID=models.AutoField(primary_key=True)
	USUARIO=models.ForeignKey(User,null=False)
	PUEBLO=models.ForeignKey('pueblo',null=False)
	DESCRIPCION=models.TextField(null=False)
	FECHA=models.DateTimeField(null=False)
	VALORACION=models.IntegerField(null=True,default=0)
	def __unicode__(self):
		return  self.USUARIO.username +' || '+self.DESCRIPCION

class evento(models.Model):
	class Meta:
		verbose_name="evento" #Nombre en singular del modelo
		verbose_name_plural="eventos" #Nombre en plural del modelo
	ID=models.AutoField(primary_key=True)
	NOMBRE=models.CharField(unique=True,null=False,max_length=50)
	FECHA=models.DateTimeField(null=False)
	PUEBLO=models.ForeignKey('pueblo',null=False)
	DESCRIPCION=models.TextField(null=False)
	LUGAR=models.CharField(null=False,max_length=50)
	IMAGEN=models.ImageField(upload_to='eventos/',null=True)
	LATITUD=models.CharField(max_length=20,null=False)
	LONGITUD=models.CharField(max_length=20,null=False)
	def __unicode__(self):
		return self.NOMBRE
	def get_evento_idioma(self,language):
		if language != settings.SELECTED_LANGUAGE:
			cont_eventos=evento_idioma.objects.filter(IDIOMA=language,EVENTO=self).count()
			if cont_eventos > 0:
				try:
					obj=evento_idioma.objects.get(IDIOMA=language,EVENTO=self)
					self.DESCRIPCION=obj.DESCRIPCION
					self.LUGAR=obj.LUGAR
				except Exception,e:
					print e
		return self

class evento_idioma(models.Model):
	class Meta:
		verbose_name="evento_idioma" #Nombre en singular del modelo
		verbose_name_plural="eventos_idiomas" #Nombre en plural del modelo
	ID=models.AutoField(primary_key=True)
	IDIOMA=models.CharField(max_length=15, null=False,blank=False,choices=IDIOMAS)
	EVENTO=models.ForeignKey('evento',null=False)
	DESCRIPCION=models.TextField(null=False)
	LUGAR=models.CharField(null=False,max_length=50)
	def __unicode__(self):
		return self.LUGAR



class comentario_evento(models.Model):
	class Meta:
		verbose_name="comentario evento" #Nombre en singular del modelo
		verbose_name_plural="comentarios de eventos" #Nombre en plural del modelo
	ID=models.AutoField(primary_key=True)
	USUARIO=models.ForeignKey(User,null=False)
	EVENTO=models.ForeignKey('evento',null=False)
	DESCRIPCION=models.TextField(null=False)
	FECHA=models.DateTimeField(null=False)
	VALORACION=models.IntegerField(null=True,default=0)
	def __unicode__(self):
		return  self.USUARIO.username +' || '+self.DESCRIPCION

class relato(models.Model):
	class Meta:
		verbose_name="relato" #Nombre en singular del modelo
		verbose_name_plural="relatos" #Nombre en plural del modelo
	ID=models.AutoField(primary_key=True)
	USUARIO=models.ForeignKey(User,null=False)
	PUEBLO=models.ForeignKey('pueblo',null=False)
	TITULO=models.CharField(null=False,max_length=30)
	DESCRIPCION=models.TextField(null=False)
	FECHA=models.DateTimeField(null=True,blank=True)
	VALORACION=models.IntegerField(null=True,default=0)
	APROBADO=models.BooleanField(null=False,default=False)
	def __unicode__(self):
		return self.PUEBLO.NOMBRE + " || " +self.USUARIO.username
	def get_relato_idioma(self,language):
		# import pdb
		# pdb.set_trace()
		if language != settings.SELECTED_LANGUAGE:
			cont_relatos=relato_idioma.objects.filter(IDIOMA=language,RELATO=self).count()
			if cont_relatos > 0:
				try:
					obj=relato_idioma.objects.get(IDIOMA=language,RELATO=self)
					self.DESCRIPCION=obj.DESCRIPCION
					self.TITULO=obj.TITULO
				except Exception,e:
					print e
		return self

class relato_idioma(models.Model):
	class Meta:
		verbose_name="relato_idioma" #Nombre en singular del modelo
		verbose_name_plural="relatos_idiomas" #Nombre en plural del modelo
	ID=models.AutoField(primary_key=True)
	RELATO=models.ForeignKey('relato',null=False)
	IDIOMA=models.CharField(max_length=15, null=False,blank=False,choices=IDIOMAS)
	TITULO=models.CharField(null=False,max_length=30)
	DESCRIPCION=models.TextField(null=False)
	def __unicode__(self):
		return self.TITULO +" || "+ self.IDIOMA.NOMBRE

class comentario_relato(models.Model):
	class Meta:
		verbose_name="comentario de relato" #Nombre en singular del modelo
		verbose_name_plural="comentarios de relatos" #Nombre en plural del modelo
	ID=models.AutoField(primary_key=True)
	USUARIO=models.ForeignKey(User,null=False)
	RELATOS=models.ForeignKey('relato',null=False)
	DESCRIPCION=models.TextField(null=False)
	FECHA=models.DateTimeField(null=False)
	VALORACION=models.IntegerField(null=True,default=0)
	def __unicode__(self):
		return  self.USUARIO.username +' || '+self.DESCRIPCION


class categoria(models.Model):
	class Meta:
		verbose_name="categoria" #Nombre en singular del modelo
		verbose_name_plural="categorias" #Nombre en plural del modelo
	ID=models.AutoField(primary_key=True)
	NOMBRE=models.CharField(unique=True,null=False,max_length=30)
	def __unicode__(self):
		return self.NOMBRE

class sitio_turistico(models.Model):
	class Meta:
		verbose_name="sitio turistico" #Nombre en singular del modelo
		verbose_name_plural="sitios turisticos" #Nombre en plural del modelo
	ID=models.AutoField(primary_key=True)
	NOMBRE=models.CharField(unique=True,null=False,max_length=50)
	DIRECCION=models.CharField(null=False,max_length=100)
	DESCRIPCION=models.TextField(null=False)
	CATEGORIA=models.ForeignKey('categoria',null=False)
	TELEFONOS=models.TextField(null=True)
	PUEBLO=models.ForeignKey('pueblo',null=False)
	IMAGEN=models.ImageField(upload_to='sitios/',null=True)
	URL=models.URLField(null=True,blank=True)
	PRECIO_DESDE= models.DecimalField(max_digits=7,decimal_places=2, null=True, default=0.00)
	PRECIO_HASTA= models.DecimalField(max_digits=7,decimal_places=2, null=True, default=0.00)
	LATITUD=models.CharField(max_length=20,null=False)
	LONGITUD=models.CharField(max_length=20,null=False)
	def __unicode__(self):
		return self.NOMBRE
	def get_sitio_turistico_idioma(self,language):
		if language != settings.SELECTED_LANGUAGE:
			cont_sitios=sitio_turistico_idioma.objects.filter(IDIOMA=language,SITIO=self).count()
			if cont_sitios > 0:
				try:
					obj=sitio_turistico_idioma.objects.get(IDIOMA=language,SITIO=self)
					self.DESCRIPCION=obj.DESCRIPCION
				except Exception,e:
					print e
		return self


class sitio_turistico_idioma(models.Model):
	class Meta:
		verbose_name="sitio_turistico_idioma" #Nombre en singular del modelo
		verbose_name_plural="sitios_turisticos_idiomas" #Nombre en plural del modelo	
	SITIO=models.ForeignKey('sitio_turistico',null=False)
	IDIOMA=models.CharField(max_length=15, null=False,blank=False,choices=IDIOMAS)
	DESCRIPCION=models.TextField(null=False)
	def __unicode__(self):
		return self.DESCRIPCION

class comentario_sitio(models.Model):
	class Meta:
		verbose_name="comentario de sitio" #Nombre en singular del modelo
		verbose_name_plural="comentarios de sitios" #Nombre en plural del modelo
	ID=models.AutoField(primary_key=True)
	USUARIO=models.ForeignKey(User,null=False)
	SITIOS=models.ForeignKey('sitio_turistico',null=False)
	DESCRIPCION=models.TextField(null=False)
	FECHA=models.DateTimeField(null=False)
	VALORACION=models.IntegerField(null=True,default=0)
	def __unicode__(self):
		return  self.USUARIO.username +' || '+self.DESCRIPCION


class contrato(models.Model):
	class Meta:
		verbose_name="contrato" #Nombre en singular del modelo
		verbose_name_plural="contratos" #Nombre en plural del modelo
	ID=models.AutoField(primary_key=True)
	SITIO=models.ForeignKey('sitio_turistico',null=False)
	OBSERVACION=models.CharField(null=True,max_length=30)
	FECHA_INICIO=models.DateField(null=False)
	DURACION=models.IntegerField(null=True,default=0)
	NOVECES=models.IntegerField(null=True,default=0)
	ULTIMA_FECHA =models.DateTimeField(null=True,blank=True)
	def __unicode__(self):
		return self.SITIO.NOMBRE+" ,contrato: "+str(self.ID)

class reporte_comentario(models.Model):
	class Meta:
		verbose_name="reporte" #Nombre en singular del modelo
		verbose_name_plural="reportes" #Nombre en plural del modelo
	ID=models.AutoField(primary_key=True)
	CLASE_COMENTARIO=models.CharField(null=False,max_length=1)
	COMENTARIO=models.IntegerField(null=True,default=0) #Cambiar a PositiveIntegerField
	RAZON=models.TextField(null=False)
	FECHA=models.DateTimeField(null=True,blank=True)
	USUARIO=models.ForeignKey(User,null=False)
	def __unicode__(self):
		return str(self.ID)

class votacion(models.Model):
	class Meta:
		verbose_name="votacion" #Nombre en singular del modelo
		verbose_name_plural="votaciones" #Nombre en plural del modelo
	ID=models.AutoField(primary_key=True)
	VOTADO=models.IntegerField(null=True,default=0) #El objeto de la votacion: relato, sitio,
	TIPO_COMENTARIO=models.CharField(max_length=1,null=False)
	VOTACION = models.BooleanField(null=False)
	USUARIO=models.ForeignKey(User,null=False)
	def __unicode__(self):
		return self.VOTACION	

class curiosidad_idioma(models.Model):
	class Meta:
		verbose_name="curiosidad_idioma" #Nombre en singular del modelo
		verbose_name_plural="curiosidades_idiomas" #Nombre en plural del modelo
	ID=models.AutoField(primary_key=True)
	IDIOMA=models.CharField(max_length=15, null=False,blank=False,choices=IDIOMAS)
	CURIOSIDAD =models.ForeignKey('curiosidad',null=False)
	TITULO=models.CharField(null=False,max_length=30)
	DESCRIPCION=models.TextField(null=False)	
	def __unicode__(self):
		return self.TITULO

class curiosidad(models.Model):
	class Meta:
		verbose_name="curiosidad" #Nombre en singular del modelo
		verbose_name_plural="curiosidades " #Nombre en plural del modelo
	ID=models.AutoField(primary_key=True)
	TITULO=models.CharField(null=False,max_length=30)
	DESCRIPCION=models.TextField(null=False)
	PUEBLO=models.ForeignKey('pueblo',null=False)
	def __unicode__(self):
		return self.TITULO
	def get_curiosidad_idioma(self,language):
		if language != settings.SELECTED_LANGUAGE:
			cont_curiosidad=curiosidad_idioma.objects.filter(IDIOMA=language,CURIOSIDAD=self).count()
			if cont_curiosidad > 0:
				try:
					obj=curiosidad_idioma.objects.get(IDIOMA=language,CURIOSIDAD=self)
					self.DESCRIPCION=obj.DESCRIPCION
					self.TITULO=obj.TITULO
				except Exception,e:
					print e
		return self

class login(models.Model):
	class Meta:
		verbose_name="Acceso" #Nombre en singular del modelo
		verbose_name_plural="Accesos " #Nombre en plural del modelo
	ID=models.AutoField(primary_key=True)
	USUARIO = models.ForeignKey(User,null=False)
	FECHA = models.DateTimeField(null=True,blank=True)