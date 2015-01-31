from django.conf.urls import patterns, include, url
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from users.views import listUser,userUpdate
admin.autodiscover()

urlpatterns = patterns('',
	    				url(r'^admin/', include(admin.site.urls)),)

urlpatterns += patterns('proyectoFinal.users.views',
						url(r'^register/?$', 'register'),
						url(r'^users/?$', listUser.as_view()),)