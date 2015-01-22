from django.conf.urls import patterns, include, url
from citys import views
from users import views
from users.views import listUser,userUpdate
from users.models import User

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
	
urlpatterns = patterns('',
	    				url(r'^admin/', include(admin.site.urls)),
	    				)

urlpatterns += patterns('proyectoFinal.users.views',
						url(r'^register/?$', 'register'),
						url(r'^users/?$', listUser.as_view()),)