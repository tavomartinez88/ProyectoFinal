from django.db.models import Q
from django.shortcuts import render_to_response
from models import Team
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.core.context_processors import csrf # to increase security in the page
from django.template import RequestContext
from proyectoFinal.users.models import User

class TeamCreate(CreateView):
	model = Team
	fields = ['name', 'captain', 'players']
	success_url = '/teams'

class listTeams(ListView):
	template_name = 'teams/listTeams.html'
	model = Team
	context_object_name = 'teams' # Nombre de la lista a recorrer desde listUsers.html

	def get_context_data(self, **kwargs):
		ctx = super(listTeams, self).get_context_data(**kwargs)
		ctx['users'] = User.objects.all()
		return ctx

class updateTeam(UpdateView):
	model = Team
	fields = ['name', 'captain', 'players']
	template_name_suffix = '_update_form' # This is: modelName_update_form.html
	success_url = '/teams'

class deleteTeam(DeleteView):
	model = Team
	success_url = '/teams'
