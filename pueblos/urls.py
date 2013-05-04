from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'pueblos.views.home', name='home'),
    # url(r'^pueblos/', include('pueblos.foo.urls')),


    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'principal.views.home'),
    url(r'^secciones/$', 'principal.views.secciones'),
    url(r'^pueblos/$', 'principal.views.pueblos'),
    url(r'^galerias/$', 'principal.views.galerias'),
    url(r'^libros/$', 'principal.views.libros'),
    url(r'^accesos/$', 'principal.views.accesos'),
    url(r'^mapa/$', 'principal.views.mapa'),
    url(r'^alojamiento/$', 'principal.views.alojamiento'),
    url(r'^comida/$', 'principal.views.comida'),
    url(r'^info/$', 'principal.views.info'),
    url(r'^dir/$', 'principal.views.dir'),
)
