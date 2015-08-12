from django.db.models import Q
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.core.context_processors import csrf # to increase security in the site
from django.template import RequestContext
from models import Tournament
from forms import TournamentForm
from proyectoFinal.fixtures.models import Fixture
from proyectoFinal.users.models import UserProfile
from proyectoFinal.complexes.models import Complex
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import Http404

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
    		usuario = UserProfile.objects.get(user=self.request.user)
    		if usuario.userType=='PR':
    			return super(TournamentCreate, self).dispatch(*args, **kwargs)
    		else:
    			raise Http404
    		

class listTournaments(ListView):
	template_name = 'tournaments/listTournaments.html'
	model = Tournament
	context_object_name = 'tournaments' # Nombre de la lista a recorrer desde listReservations.html

class markAsFinished(UpdateView):
	model = Tournament
	#fields = ['inProgress', 'teams', 'fixture']
	template_name_suffix = '_update_form' # This is: modelName_update_form.html
	success_url = '/tournaments'

	#restricted area for anonymous users
	@method_decorator(login_required)
   	def dispatch(self, *args, **kwargs):
   		usuario = UserProfile.objects.get(user = self.request.user)
   		if usuario.userType=='PR':
   			return super(markAsFinished, self).dispatch(*args, **kwargs)
   		else:
   			raise Http404
   		

   	def get_object(self, queryset=None):
		tournament = super(markAsFinished,self).get_object()
		usuario = UserProfile.objects.get(user=self.request.user)
		count_tournaments = Tournament.objects.filter(id=tournament.id,complex=Complex.objects.filter(user=self.request.user)).count()
		if self.request.user.is_anonymous():
			raise Http404
		else:
			if usuario.userType=='CM':
				raise Http404
			else:
				if count_tournaments==1:
					return tournament
				else:
					raise Http404



@login_required
def deleteTournament(request):
	usuario = UserProfile.objects.get(user=request.user)
	if usuario.userType=='PR':
		raise Http404
	else:
		tournaments = Tournament.objects.filter(complex=Complex.objects.filter(user=request.user))
		return render_to_response('tournaments/deleteAnyTournaments.html',{"tournaments": tournaments})

	


class cancelTournament(DeleteView):
	model = Tournament
	success_url = '/tournaments'

	def get_form_kwargs(self):
		usuario = UserProfile.objects.get(user=request.user)
		if usuario.userType=='PR':
			kwargs = super(cancelTournament, self).get_form_kwargs()
   			kwargs.update({'user': self.request.user})
   			return kwargs
   		raise Http404

    	

	#restricted area for anonymous users
	@method_decorator(login_required)
    	def dispatch(self, *args, **kwargs):
    		usuario = UserProfile.objects.get(user=self.request.user)
    		if usuario.userType=='PR':
    			return super(cancelTournament, self).dispatch(*args, **kwargs)
    		else:
    			raise Http404
    		


def searchTournament(request):
  query = request.GET.get('q', '')
  if query:
	qset = (Q(name__icontains=query))
	results = Tournament.objects.filter(qset).distinct()

  else:
	results = []
  return render_to_response("tournaments/searchTournament.html",{"results": results,"query": query})