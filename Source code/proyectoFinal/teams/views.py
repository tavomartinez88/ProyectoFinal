from django.db.models import Q
from django.shortcuts import render_to_response
from models import Team
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.core.context_processors import csrf # to increase security in the site
from django.template import RequestContext
from proyectoFinal.users.models import UserProfile
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import Http404


class TeamCreate(CreateView):
	model = Team
	fields = ['name', 'players']
	success_url = '/teams'

	#restricted area for anonymous users
	@method_decorator(login_required)
    	def dispatch(self, *args, **kwargs):
    		usuario = UserProfile.objects.get(user = self.request.user)   		
    		if usuario.userType=='CM' :
    			return super(TeamCreate, self).dispatch(*args, **kwargs)
    		else:
    			raise Http404
    		
	
	#set the user that's logged in as the captain
	def form_valid(self, form):
   		form.instance.captain = self.request.user
   		return super(TeamCreate, self).form_valid(form)


class listTeams(ListView):
	template_name = 'teams/listTeams.html'
	model = Team
	context_object_name = 'teams' # Nombre de la lista a recorrer desde listUsers.html

	def teams(request):
		context = RequestContext(request)
		teams = Teams.objects.order_by('name') # get all the teams
		players = User.objects.order_by('lastname') # get all the players
		context_dic = {'teams': teams, 'players': players}
		return render_to_response('/teams.html', context_dic, context)

def updateteams(request):
	usuario = UserProfile.objects.get(user=request.user)
	if not (usuario.userType=='PR' or request.user.is_anonymous()):
		teams = Team.objects.filter(captain = request.user.id)
		return render_to_response('teams/updateAnyTeams.html',{'teams': teams})
	else:
		raise Http404

class updateTeam(UpdateView):
	model = Team
	fields = ['name', 'captain', 'players']
	template_name_suffix = '_update_form' # This is: modelName_update_form.html
	success_url = '/teams'
	def get_form_kwargs(self):
		kwargs = super(updateTeam,self).get_form_kwargs()
		return kwargs

	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		usuario = UserProfile.objects.get(user=self.request.user)
		if usuario.userType=='CM':
			return super(updateTeam,self).dispatch(*args, **kwargs)
		else:
			raise Http404
		

	def get_object(self, queryset=None):
		team = super(updateTeam,self).get_object()
		
		if not team.captain == self.request.user:
			raise Http404
		return team


def deleteteams(request):
	if not (request.user.is_staff or request.user.is_anonymous()):
		teams = Team.objects.filter(captain = request.user.id)
		return render_to_response('teams/deleteAnyTeams.html',{'teams': teams})
	else:
		raise Http404

class deleteTeam(DeleteView):
	model = Team
	success_url = '/teams'
	def get_form_kwargs(self):
		kwargs = super(deleteTeam,self).get_form_kwargs()
		return kwargs

	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		usuario = UserProfile.objects.get(user=self.request.user)
		if usuario.userType=='CM':
			return super(deleteTeam,self).dispatch(*args, **kwargs)
		else:
			raise Http404
		

	def get_object(self, queryset=None):
		team = super(deleteTeam,self).get_object()
		
		if not team.captain == self.request.user:
			raise Http404
		return team	

def searchTeam(request):
  query = request.GET.get('q', '')
  if query:
	qset = (Q(name__icontains=query))
	results = Team.objects.filter(qset).distinct()

  else:
	results = []
  return render_to_response("teams/searchTeam.html",{"results": results,"query": query})

