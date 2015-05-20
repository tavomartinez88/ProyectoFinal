from django.db.models import Q
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.core.context_processors import csrf # to increase security in the site
from django.template import RequestContext
from models import Tournament
from proyectoFinal.fixtures.models import Fixture
from proyectoFinal.users.models import UserProfile
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from forms import TournamentForm

class TournamentCreate(CreateView):
	model = Tournament
	success_url = '/newfixture'
	form_class = TournamentForm

	def get_form_kwargs(self):
    		kwargs = super(TournamentCreate, self).get_form_kwargs()
    		kwargs.update({'user': self.request.user})
    		return kwargs

	#restricted area for anonymous users
	@method_decorator(login_required)
    	def dispatch(self, *args, **kwargs):
    	    return super(TournamentCreate, self).dispatch(*args, **kwargs)

class listTournaments(ListView):
	template_name = 'tournaments/listTournaments.html'
	model = Tournament
	context_object_name = 'tournaments' # Nombre de la lista a recorrer desde listReservations.html

class markAsFinished(UpdateView):
	model = Tournament
	#fields = ['inProgress', 'teams', 'fixture']
	template_name_suffix = '_update_form' # This is: modelName_update_form.html
	success_url = '/tournaments'

	def get_form_kwargs(self):
    		kwargs = super(markAsFinished, self).get_form_kwargs()
    		kwargs.update({'user': self.request.user})
    		return kwargs

	#restricted area for anonymous users
	@method_decorator(login_required)
    	def dispatch(self, *args, **kwargs):
    	    return super(markAsFinished, self).dispatch(*args, **kwargs)	



class cancelTournament(DeleteView):
	model = Tournament
	success_url = '/tournaments'

	def get_form_kwargs(self):
    		kwargs = super(cancelTournament, self).get_form_kwargs()
    		kwargs.update({'user': self.request.user})
    		return kwargs

	#restricted area for anonymous users
	@method_decorator(login_required)
    	def dispatch(self, *args, **kwargs):
    	    return super(cancelTournament, self).dispatch(*args, **kwargs)	

def searchTournament(request):
  query = request.GET.get('q', '')
  if query:
	qset = (Q(name__icontains=query))
	results = Tournament.objects.filter(qset).distinct()

  else:
	results = []
  return render_to_response("tournaments/searchTournament.html",{"results": results,"query": query})