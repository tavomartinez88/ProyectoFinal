from django.conf.urls import patterns, include, url
from complejos import views
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    					url(r'^admin/', include(admin.site.urls)),
    					url(r'^search-form/', 'complejos.views.search_form', name='search_form'),
    					url(r'^crear-form/', 'complejos.views.crear_form', name='crear_form'),
    					url(r'^eliminar-form/', 'complejos.views.eliminar_form', name='eliminar_form'),)