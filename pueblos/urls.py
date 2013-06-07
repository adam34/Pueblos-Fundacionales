from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = i18n_patterns('',
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

    url(r'^$', 'principal.views.home',name='home'),
    url(r'^secciones/$', 'principal.views.secciones',name='secciones'),
    url(r'^pueblos/$', 'principal.views.pueblos',name='pueblos'),
    url(r'^galerias/$', 'principal.views.galerias',name='galerias'),
    url(r'^mas-visto/$', 'principal.views.masvisto',name='masvisto'),
    url(r'^descubra-bcs/$', 'principal.views.descubrabcs',name='descubrabcs'),
    url(r'^bcs-desconocida/$', 'principal.views.bcsdesconocida',name='bcsdesconocida'),
    url(r'^libros/$', 'principal.views.libros',name='libros'),
    url(r'^accesos/$', 'principal.views.basico',name='basico'),
    url(r'^mapa/$', 'principal.views.mapa',name='mapa'),
    url(r'^alojamiento/$', 'principal.views.alojamiento',name='alojamiento'),
    url(r'^comida/$', 'principal.views.comida',name='comida'),
    url(r'^info/$', 'principal.views.info',name='info'),
    url(r'^dir/$', 'principal.views.dir',name='dir'),
    url(r'^politicas/$', 'principal.views.politicas',name='politicas'),
    url(r'^humans\.txt$', 'principal.views.humans',name='humans'),
    url(r'^libreria/$', 'principal.views.libreria',name='libreria'),
    url(r'^pueblos/purisima/$', 'principal.views.p',name='p'),
    url(r'^pueblos/loreto/$', 'principal.views.l',name='l'),
    url(r'^libreria/libro_purisima/$', 'principal.views.libro_p',name='libro_p'),
    url(r'^multimedia/$', 'principal.views.multimedia',name='multimedia'),
    url(r'^multimedia/player/$', 'principal.views.player',name='player'),
    url(r'^multimedia/audio/$', 'principal.views.audio',name='audio'),
    url(r'^eventos/$', 'principal.views.eventos',name='eventos'),
    url(r'^multimedia/galeria/$', 'principal.views.galeria_2',name='galeria_2'),
    url(r'^relatos/$', 'principal.views.relatos',name='relatos'),
    url(r'^sitios_turisticos/$', 'principal.views.sitiosT',name='sitios_turisticos'),
    url(r'^busqueda/$', 'principal.views.busqueda',name='busqueda'),
    url(r'^curiosidades/$', 'principal.views.curiosidades',name='curiosidades'),
    url(r'^galerias_ajax/$','principal.views.galerias_ajax', name='galerias_ajax'),
    url(r'^login_ajax/$', 'principal.views.login_ajax', name='login_ajax'),
    url(r'^registro_usuario_ajax/$', 'principal.views.registro_usuario_ajax', name='registro_usuario_ajax'),
    url(r'^recupera_ajax/$', 'principal.views.recupera_ajax', name='recupera_ajax'),
    url(r'^cerrar_sesion/$', 'principal.views.cerrar_sesion',name='cerrar_sesion'),
    url(r'^eventos_ajax/$', 'principal.views.eventos_ajax', name='eventos_ajax'),
    url(r'^comentarios_relatos_ajax/$', 'principal.views.comentarios_relatos_ajax', name='comentarios_relatos_ajax'),
    url(r'^valorar_relatos_ajax/$', 'principal.views.valorar_relatos_ajax', name='valorar_relatos_ajax'),
    url(r'^comentarios_eventos_ajax/$', 'principal.views.comentarios_eventos_ajax', name='comentarios_eventos_ajax'),
    url(r'^comentarios_sitios_ajax/$', 'principal.views.comentarios_sitios_ajax', name='comentarios_sitios_ajax'),
    url(r'^pueblos_ajax/$', 'principal.views.pueblos_ajax', name='pueblos_ajax'),
    url(r'^reporte_comentarios_ajax/$', 'principal.views.reporte_comentarios_ajax', name='reporte_comentarios_ajax'),
    url(r'^enviar_relatos_ajax/$', 'principal.views.enviar_relatos_ajax', name='enviar_relatos_ajax'),
    )
