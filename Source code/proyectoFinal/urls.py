from django.conf.urls import patterns, include, url
from django.contrib import admin
from complexes.views import listComplex,updateComplex, deleteComplex
from teams.views import TeamCreate, listTeams, updateTeam, deleteTeam
from matches.views import deleteMatch , addResult
from users.views import userUpdate, telephoneUpdate, deleteUser
from contacts.views import contactomail
from reservations.views import CreateReservationAsCommonUser, CreateReservationAsOwnerUser, listReservations, markAsAttended, cancelReservation
from courts.views import updateCourt, deleteCourt, CreateCourt
from tournaments.views import TournamentCreate, listTournaments, markAsFinished, cancelTournament, searchTournament
from fixtures.views import FixtureCreate, listFixtures, updateFixture, searchFixtures
from fixtures.views import deleteFixture
from playersinfo.views import listPlayersInfo, updatePlayerInfo, searchPlayerInfo
from publicities.views import nueva_publicidad, listPublish, update_publish, deletePublicity
from django.views.generic import TemplateView 
from django.conf.urls.static import static
from django.conf import settings
admin.autodiscover()





urlpatterns = patterns('',
	    				url(r'^admin/', include(admin.site.urls)),
	    				(r'^$', TemplateView.as_view(template_name="index.html"),{}),
	    				url(r'^login/$', 'proyectoFinal.views.login_page', name="login"),
	    				url(r'^salir/$', 'proyectoFinal.views.logout_page', name="logout"),)

urlpatterns += patterns('proyectoFinal.users.views',
						url(r'^register/?$', 'register'),
						url(r'^update_user/(?P<pk>\d+)/$', userUpdate.as_view(),name='updateuser'), #(?P<pk>\d+) -> ID for the user. This has to be changed when the login implemented
						url(r'^update_telephone/(?P<pk>\d+)/$', telephoneUpdate.as_view()),
						url(r'^delete_user/(?P<pk>\d+)/$', deleteUser.as_view()),
						) 

urlpatterns += patterns('proyectoFinal.contacts.views',
						url(r'^send_mail/?$', 'contactomail'),)

urlpatterns += patterns('proyectoFinal.complexes.views',
						url(r'^newcomplex/?$', 'register'),
						url(r'^searchcomplex/?$', 'search_complex'),
						url(r'^complexes/?$', listComplex.as_view(),name='complexes'),
						url(r'^updatecomplex/(?P<pk>\d+)/$', updateComplex.as_view()),
						url(r'^deletecomplex/(?P<pk>\d+)/$', deleteComplex.as_view()),) 

urlpatterns += patterns('proyectoFinal.courts.views',
						url(r'^addCourt/?$', CreateCourt.as_view(),name='createcourt'),
						url(r'^searchcourt/?$', 'search_court'),
						url(r'^courts/(?P<idcomplex>\d+)$', 'listCourt',name='courts'),
						url(r'^editCourt/(?P<pk>\d+)/$', updateCourt.as_view(),name='editcourt'),
						url(r'^deletecourt/(?P<pk>\d+)/$', deleteCourt.as_view(),name='deletecourt'),) 

urlpatterns += patterns('proyectoFinal.teams.views',
						url(r'^newteam/?$', TeamCreate.as_view()),
						url(r'^teams/?$', listTeams.as_view(),name='teams'),
						url(r'^updateteam/(?P<pk>\d+)/$', updateTeam.as_view()),
						url(r'^deleteteam/(?P<pk>\d+)/$', deleteTeam.as_view()),
						url(r'^searchteam/?$', 'searchTeam'),
						url(r'^playersteam/(?P<idteam>\d+)/(?P<idtournament>\d+)/$', 'playersTeam', name='players'),
						url(r'^players/(?P<idteam>\d+)$', 'playersOfTeam', name='playersforteam'),)


urlpatterns += patterns('proyectoFinal.reservations.views',
						url(r'^newreservation/?$', 'reservationCreate'),
						url(r'^addreservationCommonUser/?$', CreateReservationAsCommonUser.as_view()),
						url(r'^addreservationOwnerUser/?$', CreateReservationAsOwnerUser.as_view()),
						url(r'^reservations/?$', listReservations.as_view(), name='reservations'),
						url(r'^updatereservation/(?P<pk>\d+)/$', markAsAttended.as_view(),name='updatereservation'),
						url(r'^cancelreservation/(?P<id_reservation>\d+)/$', 'cancelReservation'))

urlpatterns += patterns('proyectoFinal.matches.views',
						url(r'^addmatch/(?P<idfixture>\d+)','addmatch',name="addmatch"),
						url(r'^deletematch/(?P<pk>\d+)/$', deleteMatch.as_view()),
						url(r'^addscore/(?P<pk>\d+)/$', addResult.as_view()),
						url(r'^searchmatch/?$', 'searchMatch'),
						url(r'^listmatchesforfixture/(?P<idfixture>\d+)','listMatchForFixture',name="list_matches"),)

urlpatterns += patterns('proyectoFinal.tournaments.views',
						url(r'^newtournament/?$', TournamentCreate.as_view()),
						url(r'^tournaments/?$', listTournaments.as_view(),name="tournaments"),
						url(r'^updatetournament/(?P<pk>\d+)/$', markAsFinished.as_view()),
						url(r'^canceltournament/(?P<pk>\d+)/$', cancelTournament.as_view()),
						url(r'^searchtournament/?$', 'searchTournament'),
						url(r'^teamsinscriptions/(?P<idtournament>\d+)$', 'teamsinscriptions', name='miteams'),)




urlpatterns += patterns('proyectoFinal.fixtures.views',
						url(r'^newfixture/?$', FixtureCreate.as_view()),
						url(r'^fixtures/?$', listFixtures.as_view()),
						url(r'^updatefixture/(?P<pk>\d+)/$', updateFixture.as_view()),
						url(r'^deletefixture/(?P<idfixture>\d+)/$', 'deleteFixture'),
						url(r'^searchfixture/?$', 'searchFixtures'),)

urlpatterns += patterns('proyectoFinal.playersinfo.views',
						url(r'^playersinfo/?$', listPlayersInfo.as_view(),name = 'listplayerinfo'),
						url(r'^searchplayerinfo/?$', 'searchPlayerInfo'),
						url(r'^editPlayer/(?P<pk>\d+)/$', updatePlayerInfo.as_view(),name = 'updateplayerinfo'),
						url(r'^addplayerinfo/(?P<idplayer>\d+)/(?P<idtournament>\d+)$','addplayerinfo',name="addplayerinfo"),					
						url(r'^info/(?P<idplayer>\d+)/(?P<idtournament>\d+)$','info',name="info"),)


urlpatterns += patterns('proyectoFinal.publicities.views',
						url(r'^newpublish/?$', 'nueva_publicidad'),
						url(r'^publicities/?$', listPublish.as_view(),name='publicaciones'),
						url(r'^updatepublish/(?P<idpublicidad>\d+)$', 'update_publish'),
						url(r'^deletepublish/(?P<pk>\d+)$', deletePublicity.as_view()),
						)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

