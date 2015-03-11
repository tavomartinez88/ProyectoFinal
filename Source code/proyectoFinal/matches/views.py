#from django.shortcuts import render
from django.db.models import Q
from django.shortcuts import render_to_response
from models import Team , Match

from django.http import HttpResponseRedirect
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.core.context_processors import csrf # to increase security in the page
from django.template import RequestContext
from django.contrib import admin


class MatchCreate(CreateView):
	model = Match
	fields = ['day', 'hour', 'minutes', 'teamlocal' , 'teamVisitant']
	success_url = '/matches'

class listMatches(ListView):
	template_name = 'matches/listMatches.html'
	model = Match
	context_object_name = 'matches' # Nombre de la lista a recorrer desde listMatches.html	


class deleteMatch(DeleteView):
	model = Match
	success_url = '/matches'

class addResult(UpdateView):
	model = Match
	fields = ['score']
	template_name_suffix = '_update_form' # This is: modelName_update_form.html
	success_url = '/matches'

def searchMatch(request):
	#Class.objects.filter(date=datetime(2008,9,4)).query.as_sql()
  query = request.GET.get('q', '')
  if query:
	qset = (Q(day=query))
	results = Match.objects.filter(qset)

  else:
	results = []
  return render_to_response("matches/searchMatch.html",{"results": results,"query": query})			