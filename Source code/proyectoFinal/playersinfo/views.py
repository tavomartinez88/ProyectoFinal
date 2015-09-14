#encoding:utf-8
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
from proyectoFinal.publicities.models import Publicity
from proyectoFinal.teams.models import Team
from forms import PlayerForm
from django.http import Http404
from django.shortcuts import get_object_or_404


"""
Esta vista crea una estadistica asociada a un jugador y a un torneo en el cual participa.
El usuario quien registra la estadistica debe estar logueado y ademas tener permisos 
de usuario propietario
"""
def addplayerinfo(request, idplayer, idtournament):
	if request.user.is_anonymous():
		return HttpResponseRedirect('/login')
	try:
		usuario = UserProfile.objects.get(user=request.user)
	except Exception:
		return HttpResponseRedirect('/login')
	if usuario.userType == 'PR':
		try:
			publish_one = Publicity.objects.all().order_by('?').first()
		except Exception:
			publish_one = False
		try:
			publish_second = Publicity.objects.all().exclude(id=publish_one.id).order_by('?').first()
		except Exception:
			publish_second = False				
		if request.POST:
			mform = PlayerForm(request.POST)		
			if mform.is_valid(): #if the information in the form its correct
				#First, save the default User model provided by Django
				player = PlayersInfo(
                		goals=mform.cleaned_data['goals'],
						yellowCards=mform.cleaned_data['yellowCards'], 
						redCards=mform.cleaned_data['redCards'],
						user=UserProfile.objects.get(user_id=idplayer),
						tournament= Tournament.objects.get(id=idtournament),					
                		)
				
				if usuario.userType == 'PR' and usuario.user == player.tournament.complex.user:
					player.save()
			return HttpResponseRedirect('/playersinfo')
		else:
			mform = PlayerForm()
			player_id = UserProfile.objects.get(id=idplayer)
		return render_to_response('playersinfo/addplayerinfo.html', {'mform': mform, 'player_id':player_id,'idtournament':idtournament,'publish_one':publish_one,'publish_second':publish_second}, RequestContext(request, {}))
	else:
		message = """
				  Oops!!! ha ocurrido un inconveniente, no tienes los permisos necesarios para crear estadisticas.
				  Si el inconveniente persiste contactese.
				  """
		sendmail = True
		return render_to_response('404.html',{'message':message,'sendmail':sendmail})

"""esta vista toma el id del jugador y si ya tiene creada la estadistica
redirige a la actualizacion de la misma, de lo contrario redirige a la creacion
de la estadistica"""
def info(request, idplayer, idtournament):
	try:
		playerForStatisticUpdate = UserProfile.objects.get(id=idplayer)
		estadistica = PlayersInfo.objects.filter(user_id=playerForStatisticUpdate.id, tournament_id=idtournament)
	except Exception:
		message = """
				  Oops!!! ha ocurrido un inconveniente,intente más tarde.Si el inconveniente persiste contactese.
				  """
		sendmail = True
		return render_to_response('404.html',{'message':message,'sendmail':sendmail})
	if estadistica.count()>0:
		stadistic = PlayersInfo.objects.get(user_id=playerForStatisticUpdate.id, tournament_id=idtournament)
		return HttpResponseRedirect('/editPlayer/'+str(stadistic.id))
	else:
		torneo = Tournament.objects.get(id=idtournament)
		return HttpResponseRedirect('/addplayerinfo/'+str(idplayer)+'/'+str(idtournament))

"""
Esta vista lista las estadisticas de los jugadores
"""
class listPlayersInfo(ListView):
	template_name = 'playersinfo/listPlayersInfo.html'
	model = PlayersInfo
	context_object_name = 'playersinfo' # Nombre de la lista a recorrer desde listPlayersInfo.html
	paginate_by = 11

	def get_queryset(self):
		if self.request.user.is_anonymous():
			return PlayersInfo.objects.none()
		else:
			usuario = UserProfile.objects.get(user_id=self.request.user)
			if usuario.userType=='PR':
				return PlayersInfo.objects.filter(tournament=Tournament.objects.filter(complex=Complex.objects.filter(user=self.request.user)))
			else:
				return PlayersInfo.objects.all()

	def get_context_data(self, **kwargs):
	    # Call the base implementation first to get a context
	    context = super(listPlayersInfo, self).get_context_data(**kwargs)
	    # Add in the publisher
	    try:
	    	context['publish_one'] = Publicity.objects.all().order_by('?').first()
	    except Exception:
	    	context['publish_one'] = False
	    try:
	    	context['publish_second'] = Publicity.objects.all().exclude(id=context['publish_one'].id).order_by('?').first()
	    except Exception:
	    	context['publish_second'] = False
	    return context					
		
		
"""
Esta vista actualiza la estadistica de un jugador en un torneo 
"""
class updatePlayerInfo(UpdateView):
	model = PlayersInfo
	template_name_suffix = '_update_form' # This is: modelName_update_form.html
	success_url = '/playersinfo'
	form_class = PlayerForm

  	def get_form_kwargs(self):
  		kwargs = super(updatePlayerInfo, self).get_form_kwargs()
  		return kwargs	

	
  	def dispatch(self, *args, **kwargs):
  		if self.request.user.is_anonymous():
  			return HttpResponseRedirect('/login')
  		else:
  			try:
  				usuario = UserProfile.objects.get(user=self.request.user)
  				if usuario.userType=='PR':
  					return super(updatePlayerInfo, self).dispatch(*args, **kwargs)
  				else:
  					message = """
  							  Oops!!! ha ocurrido un inconveniente, no tienes los permisos necesarios 
  							  para poder actualizar las estadisticas del jugador, intente más tarde.
  							  Si aún persiste el inconveniente contactese
  							  """
  					sendmail = True
  					return render_to_response('404.html',{'message':message,'sendmail':sendmail})  				
  			except Exception:
  				return HttpResponseRedirect('/login')

	def get_object(self, querySet=None):
		estadistica = super(updatePlayerInfo, self).get_object()
		torneo = Tournament.objects.get(id=estadistica.tournament_id)
		complejo = Complex.objects.get(id= torneo.complex_id)
		try:
			usuario_complex = UserProfile.objects.get(user = complejo.user)
			usuario = UserProfile.objects.get(user=self.request.user)
		except Exception:
			raise Http404
		if usuario.userType == 'PR' and  self.request.user.is_staff and usuario.user == usuario_complex.user:
			return estadistica
		else:
			message = """
					  Oops!!! ha ocurrido un inconveniente, no tienes los permisos necesarios 
					  para poder actualizar la estadisticas del jugador, intente mas tarde.
					  Si aún persiste el inconveniente 
					  """
			sendmail = True
			return render_to_response('404.html',{'message':message,'sendmail':sendmail})

	def get_context_data(self, **kwargs):
	    # Call the base implementation first to get a context
	    context = super(updatePlayerInfo, self).get_context_data(**kwargs)
	    # Add in the publisher
	    try:
	    	context['publish_one'] = Publicity.objects.all().order_by('?').first()
	    except Exception:
	    	context['publish_one'] = False
	    try:
	    	context['publish_second'] = Publicity.objects.all().exclude(id=context['publish_one'].id).order_by('?').first()
	    except Exception:
	    	context['publish_second'] = False
	    return context		
		
"""
Esta vista se encarga de realizar la busqueda de estadisticas
"""
def searchPlayerInfo(request):
  query = request.GET.get('q', '')
  if query:
  	try:
  		qset = (Q(user__firstname__icontains=query) | (Q(user__lastname__icontains=query)))
		results = PlayersInfo.objects.filter(qset).distinct()
  	except Exception:
  		raise Http404
  else:
	results = []
	try:
		publish_one = Publicity.objects.all().order_by('?').first()
	except Exception:
		publish_one = False
	try:
		publish_second = Publicity.objects.all().exclude(id=publish_one.id).order_by('?').first()
	except Exception:
		publish_second = False	
  return render_to_response("playersinfo/searchPlayerInfo.html",{"results": results,"query": query,'publish_one':publish_one,'publish_second':publish_second}, RequestContext(request, {}))