#from django.shortcuts import render
from django.db.models import Q
from django.shortcuts import render_to_response
from models import Team , Match , Fixture
from proyectoFinal.tournaments.models import Tournament
from proyectoFinal.complexes.models import Complex
from forms import MatchForm
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.core.context_processors import csrf # to increase security in the page
from django.template import RequestContext
from django.contrib import admin
from proyectoFinal.users.models import UserProfile
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import Http404

@login_required
def addmatch(request,idfixture):
	usuario = UserProfile.objects.get(user=request.user)
	if usuario.userType=='PR':
		if request.POST:
			mform = MatchForm(request.POST)
			fixture_id = request.GET.get('idfixture')
			if mform.is_valid(): #if the information in the form its correct
				#First, save the default User model provided by Django
				match = Match(
                		day=mform.cleaned_data['day'],
						hour=mform.cleaned_data['hour'], 
						minutes=mform.cleaned_data['minutes'],
						teamlocal=mform.cleaned_data['teamlocal'],
						teamVisitant=mform.cleaned_data['teamVisitant'],
						fixture = Fixture.objects.get(id=idfixture)
                		)
				usuario = UserProfile.objects.get(user_id=request.user)
				f = Fixture.objects.get(id=idfixture)
				if mform.cleaned_data['day']<f.date :
					raise Http404
				if usuario.userType == 'PR':
					match.save()
			return HttpResponseRedirect('/fixtures')
		else:
			mform = MatchForm()		
			#la sig variable y el if verifica si el fixture es propiedad del usuario logueado
			verify_fixture = Fixture.objects.filter(id=idfixture ,tournament=Tournament.objects.filter(complex=Complex.objects.filter(user=request.user))).count()	
			if verify_fixture == 0:
				raise Http404
			else:
				fixture_id = Fixture.objects.get(id=idfixture)
			
		return render_to_response('matches/addmatch.html', {'mform': mform, 'fixture_id':fixture_id}, RequestContext(request, {}))
	else:
		raise Http404



class listMatches(ListView):
	template_name = 'matches/listMatches.html'
	model = Match
	context_object_name = 'matches' # Nombre de la lista a recorrer desde listMatches.html	

	def get_queryset(self):
		usuario = UserProfile.objects.get(user=self.request.user)
		if usuario.userType=='PR':
			return Match.objects.filter(fixture=Fixture.objects.filter(tournament=Tournament.objects.filter(complex=Complex.objects.filter(user=self.request.user))))
		else:
			return Match.objects.all()

		


class deleteMatch(DeleteView):
	model = Match
	success_url = '/matches'

  	def get_form_kwargs(self):
  		kwargs = super(deleteMatch, self).get_form_kwargs()
  		return kwargs


	@method_decorator(login_required)
  	def dispatch(self, *args, **kwargs):
    		return super(deleteMatch, self).dispatch(*args, **kwargs)

  	def get_object(self, queryset=None):
	    #select the court object that we want to update
	    partido = super(deleteMatch, self).get_object()
	    #select the user in base of the complex
	    fixture = Fixture.objects.get(id=partido.fixture.id)
	    torneo = Tournament.objects.get(id=fixture.tournament_id)
	    complejo = Complex.objects.get(id=torneo.complex_id)
	    usuario = UserProfile.objects.get(user_id = complejo.user_id)
	    if not usuario.user == self.request.user and usuario.userType == 'PR':
	        raise Http404
	    return partido

class addResult(UpdateView):
	model = Match
	fields = ['score']
	template_name_suffix = '_update_form' # This is: modelName_update_form.html
	success_url = '/fixtures'

  	def get_form_kwargs(self):
  		kwargs = super(addResult, self).get_form_kwargs()
  		return kwargs


	@method_decorator(login_required)
  	def dispatch(self, *args, **kwargs):
    		return super(addResult, self).dispatch(*args, **kwargs)

  	def get_object(self, queryset=None):
	    #select the court object that we want to update
	    partido = super(addResult, self).get_object()
	    #select the user in base of the complex
	    fixture = Fixture.objects.get(id=partido.fixture.id)
	    torneo = Tournament.objects.get(id=fixture.tournament_id)
	    complejo = Complex.objects.get(id=torneo.complex_id)
	    usuario = UserProfile.objects.get(user_id = complejo.user_id)
	    if not usuario.user == self.request.user and usuario.userType == 'PR':
	        raise Http404
	    return partido	

def searchMatch(request):
	#Class.objects.filter(date=datetime(2008,9,4)).query.as_sql()
  query = request.GET.get('q', '')
  if query:
	qset = (Q(day=query))
	results = Match.objects.filter(qset)

  else:
	results = []
  return render_to_response("matches/searchMatch.html",{"results": results,"query": query})			