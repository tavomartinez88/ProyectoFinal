from django.conf.urls import patterns, include, url
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from complexes.views import listComplex,updateComplex, deleteComplex
from teams.views import TeamCreate, listTeams, updateTeam, deleteTeam
from matches.views import MatchCreate, listMatches , deleteMatch , addResult
from users.views import listUser,userUpdate, telephoneUpdate, deleteUser
from reservations.views import ReservationCreate, listReservations, markAsAttended, cancelReservation, searchReservation
from courts.views import listCourt, updateCourt, deleteCourt
from tournaments.views import TournamentCreate, listTournaments, markAsFinished, cancelTournament, searchTournament
from fixtures.views import FixtureCreate, listFixtures, updateFixture, deleteFixture, searchFixtures
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

urlpatterns += patterns('proyectoFinal.reservations.views',
						url(r'^newreservation/?$', ReservationCreate.as_view()),
						url(r'^reservations/?$', listReservations.as_view()),
						url(r'^updatereservation/(?P<pk>\d+)/$', markAsAttended.as_view()),
						url(r'^cancelreservation/(?P<pk>\d+)/$', cancelReservation.as_view()),
						url(r'^searchreservation/?$', 'searchReservation'),)

urlpatterns += patterns('proyectoFinal.matches.views',
						url(r'^newmatch/?$', MatchCreate.as_view()),
						url(r'^matches/?$', listMatches.as_view()),
						url(r'^deletematch/(?P<pk>\d+)/$', deleteMatch.as_view()),
						url(r'^addscore/(?P<pk>\d+)/$', addResult.as_view()),
						url(r'^searchmatch/?$', 'searchMatch'),)

urlpatterns += patterns('proyectoFinal.tournaments.views',
						url(r'^newtournament/?$', TournamentCreate.as_view()),
						url(r'^tournaments/?$', listTournaments.as_view()),
						url(r'^updatetournament/(?P<pk>\d+)/$', markAsFinished.as_view()),
						url(r'^canceltournament/(?P<pk>\d+)/$', cancelTournament.as_view()),
						url(r'^searchtournament/?$', 'searchTournament'),)

urlpatterns += patterns('proyectoFinal.fixtures.views',
						url(r'^newfixture/?$', FixtureCreate.as_view()),
						url(r'^fixtures/?$', listFixtures.as_view()),
						url(r'^updatefixture/(?P<pk>\d+)/$', updateFixture.as_view()),
						url(r'^deletefixture/(?P<pk>\d+)/$', deleteFixture.as_view()),
						url(r'^searchfixture/?$', 'searchFixtures'),)
