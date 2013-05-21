# -*- encoding: utf-8 -*-
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.


class idioma(models.Model):
	class Meta:
		verbose_name="idioma" #Nombre en singular del modelo
		verbose_name_plural="idiomas" #Nombre en plural del modelo
	ID = models.AutoField(primary_key=True, null=False)
	NOMBRE = models.CharField(max_length=20,null=False, unique=True)
	def __unicode__(self):
		return self.NOMBRE

class archivo(models.Model):
	class Meta:
		verbose_name="archivo" #Nombre en singular del modelo
		verbose_name_plural="archivos" #Nombre en plural del modelo
	FORMATOS=(
		('BMP','BMP'),
		('JPG','JPG'),
		('PNG','PNG'),
		('TIFF','TIFF'),
		('MP3','MP3'),
		('WAV','WAV'),
		('MP4','MP4'),
	)
	ID=models.AutoField(primary_key=True, null=False ,unique=True)
	NOMBRE=models.CharField(max_length=20,null=False)
	DESCRIPCION=models.CharField(max_length=100,null=False)
	TIPO=models.CharField(max_length=10,null=False,choices=FORMATOS)
	RUTA=models.FileField(upload_to='galerias/')
	def __unicode__(self):
		return self.NOMBRE

class galeria(models.Model):
	class Meta:
		verbose_name="galeria" #Nombre en singular del modelo
		verbose_name_plural="galerias" #Nombre en plural del modelo
	ID=models.AutoField(primary_key=True, null=False)
	NOMBRE=models.CharField(max_length=40,null=False)
	DESCRIPCION=models.CharField(max_length=100,null=False)
	USUARIO=models.ForeignKey(User,unique=True)
	ARCHIVOS=models.ManyToManyField(archivo)
	def __unicode__(self):
		return self.NOMBRE

#max_digits=5, decimal_places=2
class pueblo(models.Model):
	class Meta:
		verbose_name="pueblo" #Nombre en singular del modelo
		verbose_name_plural="pueblos" #Nombre en plural del modelo
	ID=models.AutoField(primary_key=True, null=False)
	NOMBRE=models.CharField(max_length=30,null=False)
	GALERIA=models.ForeignKey('galeria',null=True)
	TIPO=models.CharField(max_length=1,null=False)
	LATITUD=models.CharField(max_length=10,null=False)
	LONGITUD=models.CharField(max_length=10,null=False)
	def __unicode__(self):
		return self.NOMBRE

class pueblo_idioma(models.Model):
	class Meta:
		verbose_name="pueblo_idioma" #Nombre en singular del modelo
		verbose_name_plural="pueblos_idiomas" #Nombre en plural del modelo
	ID=models.AutoField(primary_key=True, null=False,unique=True)
	PUEBLO=models.ForeignKey('Pueblo',null=False)
	IDIOMA=models.ForeignKey('Idioma',null=False)
	DESCRIPCION=models.TextField(null=False)
	def __unicode__(self):
		return self.ID


class pueblo_administrador(models.Model):
	class Meta:
		verbose_name="pueblo_administrador" #Nombre en singular del modelo
		verbose_name_plural="pueblo_administradores" #Nombre en plural del modelo
	ID=models.AutoField(primary_key=True, null=False)
	PUEBLO=models.ForeignKey('pueblo',null=False)
	ADMINISTRADOR=models.ForeignKey(User,unique=True)
	ROL=models.CharField(max_length=10,null=False)
	def __unicode__(self):
		return self.ID

class comentario_pueblo(models.Model):
	class Meta:
		verbose_name="comentario_pueblo" #Nombre en singular del modelo
		verbose_name_plural="comentarios_pueblos" #Nombre en plural del modelo
	ID=models.AutoField(primary_key=True, null=False)
	USUARIO=models.ForeignKey(User,unique=True)
	PUEBLO=models.ForeignKey('pueblo',null=False)
	DESCRIPCION=models.TextField(null=False)
	FECHA=models.DateTimeField(null=False)
	VALORACION=models.IntegerField(null=True,default=0)
	def __unicode__(self):
		return self.ID

class evento(models.Model):
	class Meta:
		verbose_name="evento" #Nombre en singular del modelo
		verbose_name_plural="eventos" #Nombre en plural del modelo
	ID=models.AutoField(primary_key=True, null=False)
	NOMBRE=models.CharField(null=False,max_length=50)
	FECHA=models.DateTimeField(null=False)
	PUEBLO=models.ForeignKey('pueblo',null=False)
	IMAGEN=models.ImageField(upload_to='eventos/',null=True)
	LATITUD=models.CharField(max_length=10,null=False)
	LONGITUD=models.CharField(max_length=10,null=False)
	def __unicode__(self):
		return self.NOMBRE

class evento_idioma(models.Model):
	class Meta:
		verbose_name="evento_idioma" #Nombre en singular del modelo
		verbose_name_plural="eventos_idiomas" #Nombre en plural del modelo
	ID=models.AutoField(primary_key=True, null=False)
	IDIOMA=models.ForeignKey('idioma',null=False)
	EVENTO=models.ForeignKey('evento',null=False)
	DESCRIPCION=models.TextField(null=False)
	LUGAR=models.CharField(null=False,max_length=50)
	def __unicode__(self):
		return self.ID


class comentario_evento(models.Model):
	class Meta:
		verbose_name="comentario_evento" #Nombre en singular del modelo
		verbose_name_plural="comentarios_eventos" #Nombre en plural del modelo
	ID=models.AutoField(primary_key=True, null=False)
	USUARIO=models.ForeignKey(User,unique=True)
	EVENTO=models.ForeignKey('evento',null=False)
	DESCRIPCION=models.TextField(null=False)
	FECHA=models.DateTimeField(null=False)
	VALORACION=models.IntegerField(null=True,default=0)
	def __unicode__(self):
		return self.ID

class relato(models.Model):
	class Meta:
		verbose_name="relato" #Nombre en singular del modelo
		verbose_name_plural="relatos" #Nombre en plural del modelo
	ID=models.AutoField(primary_key=True, null=False)
	USUARIOS=models.ForeignKey(User,unique=True)
	PUEBLO=models.ForeignKey('pueblo',null=False)
	FECHA=models.DateTimeField(null=False)
	VALORACION=models.IntegerField(null=True,default=0)
	APROBADO=models.BooleanField(null=False,default=False)
	def __unicode__(self):
		return self.ID

class relato_idioma(models.Model):
	class Meta:
		verbose_name="relato_idioma" #Nombre en singular del modelo
		verbose_name_plural="relatos_idiomas" #Nombre en plural del modelo
	ID=models.AutoField(primary_key=True, null=False)
	RELATO=models.ForeignKey('relato',unique=True)
	IDIOMA=models.ForeignKey('idioma',unique=True)
	TITULO=models.CharField(null=False,max_length=30)
	DESCRIPCION=models.TextField(null=False)
	def __unicode__(self):
		return self.TITULO

class comentario_relato(models.Model):
	class Meta:
		verbose_name="comentario_relato" #Nombre en singular del modelo
		verbose_name_plural="comentarios_relatos" #Nombre en plural del modelo
	ID=models.AutoField(primary_key=True, null=False)
	USUARIO=models.ForeignKey(User,unique=True)
	RELATOS=models.ForeignKey('relato',null=False)
	DESCRIPCION=models.TextField(null=False)
	FECHA=models.DateTimeField(null=False)
	VALORACION=models.IntegerField(null=True,default=0)
	def __unicode__(self):
		return self.ID


class categoria(models.Model):
	class Meta:
		verbose_name="categoria" #Nombre en singular del modelo
		verbose_name_plural="categorias" #Nombre en plural del modelo
	ID=models.AutoField(primary_key=True, null=False)
	NOMBRE=models.CharField(null=False,max_length=30)
	def __unicode__(self):
		return self.NOMBRE

class sitio_turistico(models.Model):
	class Meta:
		verbose_name="sitio turistico" #Nombre en singular del modelo
		verbose_name_plural="sitios turisticos" #Nombre en plural del modelo
	ID=models.AutoField(primary_key=True, null=False)
	NOMBRE=models.CharField(null=False,max_length=50)
	DIRECCION=models.TextField(null=False)
	CATEGORIA=models.ForeignKey('categoria',null=False)
	TELEFONOS=models.TextField(null=False)
	USUARIO=models.ForeignKey(User,unique=True)
	PUEBLO=models.ForeignKey('pueblo',null=False)
	IMAGEN=models.ImageField(upload_to='sitios/',null=True)
	LATITUD=models.CharField(max_length=10,null=False)
	LONGITUD=models.CharField(max_length=10,null=False)
	def __unicode__(self):
		return self.NOMBRE

class sitio_turistico_idioma(models.Model):
	class Meta:
		verbose_name="sitio_turistico_idioma" #Nombre en singular del modelo
		verbose_name_plural="sitios_turisticos_idiomas" #Nombre en plural del modelo	
	SITIO=models.ForeignKey('sitio_turistico',null=False,unique=True)
	IDIOMA =models.ForeignKey('idioma',unique=True)
	DESCRIPCION=models.TextField(null=False)
	def __unicode__(self):
		return self.ID

class comentario_sitio(models.Model):
	class Meta:
		verbose_name="comentario_sitio" #Nombre en singular del modelo
		verbose_name_plural="comentarios_sitios" #Nombre en plural del modelo
	ID=models.AutoField(primary_key=True, null=False)
	USUARIO=models.ForeignKey(User,unique=True)
	SITIOS=models.ForeignKey('sitio_turistico',null=False)
	DESCRIPCION=models.TextField(null=False)
	FECHA=models.DateTimeField(null=False)
	VALORACION=models.IntegerField(null=True,default=0)
	def __unicode__(self):
		return self.ID


class contrato(models.Model):
	class Meta:
		verbose_name="contrato" #Nombre en singular del modelo
		verbose_name_plural="contratos" #Nombre en plural del modelo
	ID=models.AutoField(primary_key=True, null=False)
	SITIO=models.ForeignKey('sitio_turistico',null=False)
	DESCRIPCION=models.CharField(null=False,max_length=30)
	FECHA_INICIO=models.DateTimeField(null=False)
	DURACION=models.IntegerField(null=True,default=0)
	NOVECES=models.IntegerField(null=True,default=0)
	def __unicode__(self):
		return self.ID

class reporte_comentario(models.Model):
	class Meta:
		verbose_name="reporte_comentario" #Nombre en singular del modelo
		verbose_name_plural="reportes_comentarios" #Nombre en plural del modelo
	ID=models.AutoField(primary_key=True, null=False)
	CLASE_COMENTARIO=models.CharField(null=False,max_length=1)
	COMENTARIO=models.IntegerField(null=True,default=0)
	RAZON=models.TextField(null=False)
	USUARIO=models.ForeignKey(User,unique=True)
	def __unicode__(self):
		return self.ID

class curiosidad_idioma(models.Model):
	class Meta:
		verbose_name="curiosidad_idioma" #Nombre en singular del modelo
		verbose_name_plural="curiosidades_idiomas" #Nombre en plural del modelo
	ID=models.AutoField(primary_key=True, null=False)
	IDIOMA =models.ForeignKey('idioma',null=False)
	CURIOSIDAD =models.ForeignKey('curiosidad',null=False)
	TITULO=models.CharField(null=False,max_length=30)
	DESCRIPCION=models.TextField(null=False)	
	def __unicode__(self):
		return self.TITULO

class curiosidad(models.Model):
	class Meta:
		verbose_name="curiosidad" #Nombre en singular del modelo
		verbose_name_plural="curiosidades " #Nombre en plural del modelo
	ID=models.AutoField(primary_key=True, null=False)
	PUEBLO=models.ForeignKey('pueblo',null=False)