from django.conf.urls import patterns, include, url
from complejos import views
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	    				url(r'^admin/', include(admin.site.urls)),)

urlpatterns += patterns('complejos.views',
    					url(r'^search-form/', 'search_form', name='search_form'),
    					url(r'^crear-form/', 'crear_form', name='crear_form'),
    					url(r'^eliminar-form/', 'eliminar_form', name='eliminar_form'),)

urlpatterns += patterns('jugadores.views',
	    				url(r'^search-player/', 'search_player', name='search_player'),
    					url(r'^registro/', 'registrar_jugador', name='registrar_jugador'),
    					url(r'^eliminar-jugador/', 'eliminar_jugador', name='eliminar_jugador'),
    					url(r'^players/', include('jugadores.urls', namespace="upersonas")),)
