from django.conf.urls import patterns, include, url
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from users.views import listUser,userUpdate, telephoneUpdate, deleteUser
admin.autodiscover()

urlpatterns = patterns('',
	    				url(r'^admin/', include(admin.site.urls)),)

urlpatterns += patterns('proyectoFinal.users.views',
						url(r'^register/?$', 'register'),
						url(r'^users/?$', listUser.as_view()),
						url(r'^update_user/(?P<pk>\d+)/$', userUpdate.as_view()), #(?P<pk>\d+) -> ID for the user. This has to be changed when the login implemented
						url(r'^update_telephone/(?P<pk>\d+)/$', telephoneUpdate.as_view()),
						url(r'^delete_user/(?P<pk>\d+)/$', deleteUser.as_view()),) 

