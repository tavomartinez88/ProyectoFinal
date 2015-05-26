from django.db.models import Q
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, ListView, UpdateView	
from django.core.context_processors import csrf # to increase security in the site
from django.template import RequestContext
from models import PlayersInfo
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from proyectoFinal.tournaments.models import Tournament
from proyectoFinal.complexes.models import Complex
from proyectoFinal.users.models import UserProfile
from proyectoFinal.teams.models import Team

class PlayersInfoCreate(CreateView):
	model = PlayersInfo
	success_url = '/playersinfo'
	fields = ['goals', 'yellowCards', 'redCards', 'tournament']
	#restricted area for anonymous users
	@method_decorator(login_required)
    	def dispatch(self, *args, **kwargs):
    	    return super(PlayersInfoCreate, self).dispatch(*args, **kwargs)

    	def form_valid(self, form):
    		form.instance.user = self.request.user
    		return super(PlayersInfoCreate, self).form_valid(form)

def listTournamentsForPlayersInfo(request):
	if request.user.is_staff:
		userprofile = UserProfile.objects.get(user_id=request.user)
		if userprofile.userType=='PR':
			torneos = Tournament.objects.filter(complex=Complex.objects.filter(user=request.user))
			return render_to_response('playersinfo/listTournamentsForPlayersInfo.html', {'torneos': torneos,})
		else : 
			raise Http404
	else :
		raise Http404	   

def listTeamsFromTournament(request, idtournament):
	if request.user.is_staff:
		userprofile = UserProfile.objects.get(user_id=request.user)
		if userprofile.userType=='PR':
			equipos = Team.objects.filter(tournament=idtournament)
			return render_to_response('playersinfo/teamsFromTournament.html', {'equipos': equipos,})
		else : 
			raise Http404
	else :
		raise Http404

def playersFromTeam(request, idteam):
	if request.user.is_staff:
		userprofile = UserProfile.objects.get(user_id=request.user)
		if userprofile.userType=='PR':
			equipo=Team.objects.get(id=idteam)
			jugadores = equipo.players.all()
			playerInfo = PlayersInfo.objects.all()
			return render_to_response('playersinfo/playersFromTeam.html', {'jugadores': jugadores, 'playerInfo': playerInfo,})
		else : 
			raise Http404
	else :
		raise Http404		 	

def get_playerinfo_from_userid(request, userid):
	infoJugador = PlayersInfo.objects.get(user_id=userid)
	return render_to_response('playersinfo/playersinfo_update_form.html', {'infoJugador': infoJugador,})

class listPlayersInfo(ListView):
	template_name = 'playersinfo/listPlayersInfo.html'
	model = PlayersInfo
	context_object_name = 'playersinfo' # Nombre de la lista a recorrer desde listPlayersInfo.html

class updatePlayerInfo(UpdateView):
	model = PlayersInfo
	fields = ['goals', 'yellowCards', 'redCards']
	template_name_suffix = '_update_form' # This is: modelName_update_form.html
	success_url = '/playersinfo'

	#restricted area for anonymous users
	@method_decorator(login_required)
    	def dispatch(self, *args, **kwargs):
    	    return super(updatePlayerInfo, self).dispatch(*args, **kwargs)

    	def form_valid(self, form):
    		form.instance.user = self.request.user
    		return super(updatePlayerInfo, self).form_valid(form)

def searchPlayerInfo(request):
  query = request.GET.get('q', '')
  if query:
	qset = (Q(user__firstname__icontains=query) |
		   (Q(user__lastname__icontains=query)))
	results = PlayersInfo.objects.filter(qset).distinct()

  else:
	results = []
  return render_to_response("playersinfo/searchPlayerInfo.html",{"results": results,"query": query})