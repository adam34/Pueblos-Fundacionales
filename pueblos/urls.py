from django.conf.urls import patterns, include, url
from django.conf import settings


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'pueblos.views.home', name='home'),
    # url(r'^pueblos/', include('pueblos.foo.urls')),
    url(r'^uploads/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    #Vistas para el administrador de contenidos.
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/acerca_de/', 'administrador.views.acerca_de'),
    url(r'^admin/administrador/config/', 'administrador.views.config'),
    
    #Fin de urls para el administrador de contenidos.

    url(r'^$', 'principal.views.home'),
    url(r'^secciones/$', 'principal.views.secciones'),
    url(r'^pueblos/$', 'principal.views.pueblos'),
    url(r'^galerias/$', 'principal.views.galerias'),
    url(r'^mas-visto/$', 'principal.views.masvisto'),
    url(r'^descubra-bcs/$', 'principal.views.descubrabcs'),
    url(r'^bcs-desconocida/$', 'principal.views.bcsdesconocida'),
    url(r'^libros/$', 'principal.views.libros'),
    url(r'^accesos/$', 'principal.views.basico'),
    url(r'^mapa/$', 'principal.views.mapa'),
    url(r'^alojamiento/$', 'principal.views.alojamiento'),
    url(r'^comida/$', 'principal.views.comida'),
    url(r'^info/$', 'principal.views.info'),
    url(r'^dir/$', 'principal.views.dir'),
    url(r'^politicas/$', 'principal.views.politicas'),
    url(r'^humans\.txt$', 'principal.views.humans'),
    url(r'^vista1/$', 'administrador.views.vista1'),
    url(r'^vista_ajax1/$', 'administrador.views.vista_ajax1'),
    url(r'^libreria/$', 'principal.views.libreria'),
    url(r'^pueblos/purisima/$', 'principal.views.p'),
    url(r'^pueblos/loreto/$', 'principal.views.l'),
    url(r'^libreria/libro_purisima/$', 'principal.views.libro_p'),
    url(r'^multimedia/$', 'principal.views.multimedia'),
    url(r'^multimedia/player/$', 'principal.views.player'),
    url(r'^multimedia/audio/$', 'principal.views.audio'),
    url(r'^eventos/$', 'principal.views.eventos'),
    url(r'^multimedia/galeria/$', 'principal.views.galeria_2'),
    url(r'^relatos/$', 'principal.views.relatos'),
    url(r'^sitios_turisticos/$', 'principal.views.sitiosT'),
    url(r'^busqueda/$', 'principal.views.busqueda'),
    url(r'^curiosidades/$', 'principal.views.curiosidades'),
    url(r'^galerias_ajax/$','principal.views.galerias_ajax'),
    url(r'^login_ajax/$', 'principal.views.login_ajax'),
    url(r'^registro_usuario_ajax/$', 'principal.views.registro_usuario_ajax'),
    url(r'^recupera_ajax/$', 'principal.views.recupera_ajax'),
    url(r'^cerrar_sesion/$', 'principal.views.cerrar_sesion'),
    url(r'^eventos_ajax/$', 'principal.views.eventos_ajax'),
    url(r'^comentarios_relatos_ajax/$', 'principal.views.comentarios_relatos_ajax'),
    url(r'^valorar_relatos_ajax/$', 'principal.views.valorar_relatos_ajax'),
    )