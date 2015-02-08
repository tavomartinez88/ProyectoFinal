from django.conf.urls import patterns, include, url
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from complexes.views import listComplex,updateComplex, deleteComplex
from teams.views import TeamCreate, listTeams, updateTeam, deleteTeam
from users.views import listUser,userUpdate, telephoneUpdate, deleteUser
admin.autodiscover()

from courts.views import listCourt, updateCourt, deleteCourt
admin.autodiscover()


urlpatterns = patterns('',
	    				url(r'^admin/', include(admin.site.urls)),)

urlpatterns += patterns('proyectoFinal.users.views',
						url(r'^register/?$', 'register'),
						url(r'^users/?$', listUser.as_view()),
						url(r'^update_user/(?P<pk>\d+)/$', userUpdate.as_view()), #(?P<pk>\d+) -> ID for the user. This has to be changed when the login implemented
						url(r'^update_telephone/(?P<pk>\d+)/$', telephoneUpdate.as_view()),
						url(r'^delete_user/(?P<pk>\d+)/$', deleteUser.as_view()),
						url(r'^searchuser/?$', 'searchUser'),) 

urlpatterns += patterns('proyectoFinal.complexes.views',
						url(r'^newcomplex/?$', 'register'),
						url(r'^searchcomplex/?$', 'search_complex'),
						url(r'^complexes/?$', listComplex.as_view()),
						url(r'^updatecomplex/(?P<pk>\d+)/$', updateComplex.as_view()),
						url(r'^deletecomplex/(?P<pk>\d+)/$', deleteComplex.as_view()),) 

urlpatterns += patterns('proyectoFinal.courts.views',
						url(r'^addCourt/?$', 'register'),
						url(r'^searchcourt/?$', 'search_court'),
						url(r'^courts/?$', listCourt.as_view()),
						url(r'^editCourt/(?P<pk>\d+)/$', updateCourt.as_view()),
						url(r'^deletecourt/(?P<pk>\d+)/$', deleteCourt.as_view()),) 

urlpatterns += patterns('proyectoFinal.teams.views',
						url(r'^newteam/?$', TeamCreate.as_view()),
						url(r'^teams/?$', listTeams.as_view()),
						url(r'^updateteam/(?P<pk>\d+)/$', updateTeam.as_view()),
						url(r'^deleteteam/(?P<pk>\d+)/$', deleteTeam.as_view()),
						url(r'^searchteam/?$', 'searchTeam'),)