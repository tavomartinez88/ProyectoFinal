from django.db.models import Q
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.core.context_processors import csrf # to increase security in the site
from django.template import RequestContext
from models import Tournament

class TournamentCreate(CreateView):
	model = Tournament
	fields = ['name', 'teams', 'complex']
	success_url = '/tournaments'

class listTournaments(ListView):
	template_name = 'tournaments/listTournaments.html'
	model = Tournament
	context_object_name = 'tournaments' # Nombre de la lista a recorrer desde listReservations.html

class markAsFinished(UpdateView):
	model = Tournament
	fields = ['inProgress', 'teams']
	template_name_suffix = '_update_form' # This is: modelName_update_form.html
	success_url = '/tournaments'

class cancelTournament(DeleteView):
	model = Tournament
	success_url = '/tournaments'

def searchTournament(request):
  query = request.GET.get('q', '')
  if query:
	qset = (Q(name__icontains=query))
	results = Tournament.objects.filter(qset).distinct()

  else:
	results = []
  return render_to_response("tournaments/searchTournament.html",{"results": results,"query": query})