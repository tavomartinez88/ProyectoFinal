from django.db.models import Q
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, ListView, UpdateView	
from django.core.context_processors import csrf # to increase security in the site
from django.template import RequestContext
from models import PlayersInfo

class PlayersInfoCreate(CreateView):
	model = PlayersInfo
	success_url = '/playersinfo'

class listPlayersInfo(ListView):
	template_name = 'playersinfo/listPlayersInfo.html'
	model = PlayersInfo
	context_object_name = 'playersinfo' # Nombre de la lista a recorrer desde listPlayersInfo.html

class updatePlayerInfo(UpdateView):
	model = PlayersInfo
	fields = ['goals', 'yellowCards', 'redCards']
	template_name_suffix = '_update_form' # This is: modelName_update_form.html
	success_url = '/playersinfo'

def searchPlayerInfo(request):
  query = request.GET.get('q', '')
  if query:
	qset = (Q(user__firstname__icontains=query) |
		   (Q(user__lastname__icontains=query)))
	results = PlayersInfo.objects.filter(qset).distinct()

  else:
	results = []
  return render_to_response("playersinfo/searchPlayerInfo.html",{"results": results,"query": query})