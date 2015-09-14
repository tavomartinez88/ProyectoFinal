#encoding:utf-8
from django.db.models import Q
from django.shortcuts import render_to_response
from models import Team
from proyectoFinal.tournaments.models import Tournament
from proyectoFinal.publicities.models import Publicity
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.core.context_processors import csrf # to increase security in the site
from django.template import RequestContext
from proyectoFinal.users.models import UserProfile
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import Http404
from forms import TeamFormUpdate, TeamForm



"""
Esta vista se encarga de la creacion de un equipo,para ello debe ser un usuario con permisos 
de usuario comun.Al momento de crear un equipo se fija como capitán al usuario que crea dicho
equipo.
"""
class TeamCreate(CreateView):
	model = Team
	success_url = '/teams'
	form_class = TeamForm


   	def dispatch(self, *args, **kwargs):
   		try:
   			usuario = UserProfile.objects.get(user = self.request.user)
   		except Exception:
   			message = """
   					  Oops!!! ha ocurrido un inconveniente,no tienes los permisos necesarios para 
   					  poder crear un nuevo equipo.Para mas información contactese.
   					  """
   			sendmail = True		  
   			return render_to_response('404.html',{'message':message,'sendmail':sendmail})   		
   		if usuario.userType=='CM' :
   			return super(TeamCreate, self).dispatch(*args, **kwargs)
   		else:
   			message = """
   					  Oops!!! ha ocurrido un inconveniente,no tienes los permisos necesarios para 
   					  poder crear un nuevo equipo.Para mas información contactese.
   					  """
   			sendmail = True		  
   			return render_to_response('404.html',{'message':message,'sendmail':sendmail})

	def get_context_data(self, **kwargs):
	    # Call the base implementation first to get a context
	    context = super(TeamCreate, self).get_context_data(**kwargs)
	    # Add in the publisher
	    try:
	    	context['publish_one'] = Publicity.objects.all().order_by('?').first()
	    except Exception:
	    	context['publish_one'] = False
	    try:
	    	context['publish_second'] = Publicity.objects.all().exclude(id=context['publish_one'].id).first()
	    except Exception:
	    	context['publish_second'] = False
	    return context     	

    		
	
	#set the user that's logged in as the captain
	def form_valid(self, form):
   		form.instance.captain = self.request.user
   		return super(TeamCreate, self).form_valid(form)

"""
Esta vista se encarga de la visualización de los diferentes equipos.
"""
class listTeams(ListView):
	template_name = 'teams/listTeams.html'
	model = Team
	context_object_name = 'teams' # Nombre de la lista a recorrer desde listUsers.html
	paginate_by = 6

	def get_context_data(self, **kwargs):
	    # Call the base implementation first to get a context
	    context = super(listTeams, self).get_context_data(**kwargs)
	    # Add in the publisher
	    try:
	    	context['publish_one'] = Publicity.objects.all().order_by('?').first()
	    except Exception:
	    	context['publish_one'] = False
	    try:
	    	context['publish_second'] = Publicity.objects.all().exclude(id=context['publish_one'].id).first()
	    except Exception:
	    	context['publish_second'] = False	
	    return context

"""
Esta vista retorna los jugadores de un equipo y un torneo que esta jugando 
el equipo(ambos pasados como parametros)
"""
def playersTeam(request,idteam,idtournament):
  if request.user.is_anonymous():
   	message = """
   			  Oops!!! ha ocurrido un inconveniente,no tienes los permisos necesarios para 
   			  poder ver los jugadores de este equipo.Para mas información contactese.
   			  """
   	sendmail = True		  
   	return render_to_response('404.html',{'message':message,'sendmail':sendmail})
  try:
  	team = Team.objects.get(id = idteam)
  except Exception:
  	team = None
  try:
    tournament = Tournament.objects.get(id=idtournament)
  except Exception:
   	tournament = None
  try:
  	publish_one = Publicity.objects.all().order_by('?').first()
  except Exception:
  	publish_one = False
  try:
    publish_second = Publicity.objects.all().exclude(id=publish_one.id).order_by('?').last()		
  except Exception:
  	publish_second = False
  try:
    publish_third = Publicity.objects.all().exclude(id=publish_one.id).exclude(id=publish_second.id).order_by('?').last()		
  except Exception:
  	publish_third = False    
  return render_to_response("teams/playersteam.html",{"team": team,'tournament':tournament,'publish_one':publish_one,'publish_second':publish_second,'publish_third':publish_third}, RequestContext(request, {}))

"""
Esta vista retorna los jugadores de un equipo 
"""
def playersOfTeam(request,idteam):
  if request.user.is_anonymous():
   	message = """
   			  Oops!!! ha ocurrido un inconveniente,no tienes los permisos necesarios para 
   			  poder ver los jugadores de este equipo.Para mas información contactese.
   			  """
   	sendmail = True		  
   	return render_to_response('404.html',{'message':message,'sendmail':sendmail})
  try:
  	team = Team.objects.get(id = idteam)
  except Exception:
  	team = None
  try:
  	publish_one = Publicity.objects.all().order_by('?').first()
  except Exception:
  	publish_one = False
  try:
    publish_second = Publicity.objects.all().exclude(id=publish_one.id).order_by('?').last()		
  except Exception:
  	publish_second = False
  try:
    publish_third = Publicity.objects.all().exclude(id=publish_one.id).exclude(id=publish_second.id).order_by('?').last()		
  except Exception:
  	publish_third = False  
  return render_to_response("teams/playersforteam.html",{"team": team,'publish_one':publish_one,'publish_second':publish_second,'publish_third':publish_third}, RequestContext(request, {}))

"""
Esta vista se encarga de eliminar un equipo en donde el usuario que elimina debe ser un usuario
que tiene permisos de usuario comun y ademas debe ser el capitan del equipo
"""
class updateTeam(UpdateView):
	model = Team
	form_class = TeamFormUpdate
	template_name_suffix = '_update_form' # This is: modelName_update_form.html
	success_url = '/teams'
	def get_form_kwargs(self):
		kwargs = super(updateTeam,self).get_form_kwargs()
		return kwargs

	def dispatch(self, *args, **kwargs):
		if self.request.user.is_anonymous():
			return HttpResponseRedirect('/login')
		try:
			usuario = UserProfile.objects.get(user=self.request.user)
		except Exception:
			return HttpResponseRedirect('/login')
		if usuario.userType=='CM':
			return super(updateTeam,self).dispatch(*args, **kwargs)
		else:
		   	message = """
		   			  Oops!!! ha ocurrido un inconveniente,no tienes los permisos necesarios para 
		   			  poder actualizar este equipo.Para mas información contactese.
		   			  """
		   	sendmail = True		  
		   	return render_to_response('404.html',{'message':message,'sendmail':sendmail})

	def get_context_data(self, **kwargs):
	    # Call the base implementation first to get a context
	    context = super(updateTeam, self).get_context_data(**kwargs)
	    # Add in the publisher
	    try:
	    	context['publish_one'] = Publicity.objects.all().order_by('?').first()
	    except Exception:
	    	context['publish_one'] = False
	    try:
	    	context['publish_second'] = Publicity.objects.all().exclude(id=context['publish_one'].id).first()
	    except Exception:
	    	context['publish_second'] = False
	    try:
	    	context['publish_third'] = Publicity.objects.all().exclude(id=context['publish_one'].id).exclude(id=context['publish_second'].id).first()
	    except Exception, e:
	    	context['publish_third'] = False
	    return context	    		    
		

	def get_object(self, queryset=None):
		team = super(updateTeam,self).get_object()	
		if not team.captain == self.request.user:
			raise Http404
		return team

"""
Esta vista se encarga de eliminar un equipo en donde el usuario que elimina debe ser un usuario
que tiene permisos de usuario comun y ademas debe ser el capitan del equipo
"""
class deleteTeam(DeleteView):
	model = Team
	success_url = '/teams'
	def get_form_kwargs(self):
		kwargs = super(deleteTeam,self).get_form_kwargs()
		return kwargs

	def dispatch(self, *args, **kwargs):
		try:
			usuario = UserProfile.objects.get(user=self.request.user)
		except Exception:
		   	message = """
		   			  Oops!!! ha ocurrido un inconveniente,no tienes los permisos necesarios para 
		   			  poder eliminar este equipo.Para mas información contactese.
		   			  """
		   	sendmail = True		  
		   	return render_to_response('404.html',{'message':message,'sendmail':sendmail})
		if usuario.userType=='CM':
			return super(deleteTeam,self).dispatch(*args, **kwargs)
		else:
			raise Http404

	def get_context_data(self, **kwargs):
	    # Call the base implementation first to get a context
	    context = super(deleteTeam, self).get_context_data(**kwargs)
	    # Add in the publisher
	    try:
	    	context['publish_one'] = Publicity.objects.all().order_by('?').first()
	    except Exception:
	    	context['publish_one'] = False
	    try:
	    	context['publish_second'] = Publicity.objects.all().exclude(id=context['publish_one'].id).first()
	    except Exception:
	    	context['publish_second'] = False
	    return context	    				
		

	def get_object(self, queryset=None):
		team = super(deleteTeam,self).get_object()
		
		if not team.captain == self.request.user:
			raise Http404
		return team	


"""
Esta vista se encarga de la busqueda de diferentes equipos.
"""
def searchTeam(request):
  query = request.GET.get('q', '')
  if query:
  	try:
  		qset = (Q(name__icontains=query))
		results = Team.objects.filter(qset).distinct()
  	except Exception:
  		raise Http404
  else:
	results = []
  try:
  	publish_one = Publicity.objects.all().order_by('?').first()
  except Exception:
  	publish_one = False
  try:
    publish_second = Publicity.objects.all().exclude(id=publish_one.id).order_by('?').last()		
  except Exception:
  	publish_second = False
  return render_to_response("teams/searchTeam.html",{"results": results,"query": query,'publish_one':publish_one,'publish_second':publish_second}, RequestContext(request, {}))

