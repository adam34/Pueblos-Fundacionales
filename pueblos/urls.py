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
    url(r'^admin/vista1', 'administrador.views.vista1'),
    #Fin de urls para el administrador de contenidos.

    url(r'^$', 'principal.views.home'),
    url(r'^secciones/$', 'principal.views.secciones'),
    url(r'^pueblos/$', 'principal.views.pueblos'),
    url(r'^galerias/$', 'principal.views.galerias'),
    url(r'^libros/$', 'principal.views.libros'),
    url(r'^accesos/$', 'principal.views.basico'),
    url(r'^mapa/$', 'principal.views.mapa'),
    url(r'^alojamiento/$', 'principal.views.alojamiento'),
    url(r'^comida/$', 'principal.views.comida'),
    url(r'^info/$', 'principal.views.info'),
    url(r'^dir/$', 'principal.views.dir'),
    url(r'^humans\.txt$', 'principal.views.humans'),
    url(r'^vista1/$', 'administrador.views.vista1'),
    url(r'^vista_ajax1/$', 'administrador.views.vista_ajax1'),
    url(r'^libreria/$', 'principal.views.libreria'),
    url(r'^pueblos/purisima/$', 'principal.views.p'),
    url(r'^pueblos/loreto/$', 'principal.views.l'),
    url(r'^libreria/libro_purisima/$', 'principal.views.libro_p'),
    url(r'^multimedia/$', 'principal.views.multimedia'),
    url(r'^multimedia/player/$', 'principal.views.player'),
    url(r'^eventos/$', 'principal.views.eventos'),
    url(r'^multimedia/galeria/$', 'principal.views.galeria'),
    url(r'^relatos/$', 'principal.views.relatos'),
)
