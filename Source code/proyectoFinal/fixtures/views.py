from django.db.models import Q
from django.shortcuts import render_to_response
from models import Fixture
from proyectoFinal.matches.models import Match
from proyectoFinal.users.models import UserProfile
from proyectoFinal.tournaments.models import Tournament
from proyectoFinal.complexes.models import Complex
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.core.context_processors import csrf # to increase security in the page
from django.template import RequestContext
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import Http404
from forms import FixtureForm
import datetime
from django.http import HttpResponse


class FixtureCreate(CreateView):
	model = Fixture
	success_url = '/fixtures'
	form_class = FixtureForm
	#restricted area for anonymous users
	@method_decorator(login_required)
    	def dispatch(self, *args, **kwargs):
    	    return super(FixtureCreate, self).dispatch(*args, **kwargs)

	
	def form_valid(self, form):
    		form.instance.user = self.request.user
    		return super(FixtureCreate, self).form_valid(form)
	
	def get_form_kwargs(self):
    		kwargs = super(FixtureCreate, self).get_form_kwargs()
    		kwargs.update({'user': self.request.user})
    		return kwargs    		
	
def listMatchForFixture(request,idfixture):
		if request.user.is_staff:
			userprofile = UserProfile.objects.get(user_id=request.user)
			if userprofile.userType=='PR':
				fix = Fixture.objects.get(id=idfixture)
				partidos = Match.objects.filter(fixture_id=fix.id)
				return render_to_response('fixtures/listMatchForFixture.html', {'partidos': partidos, 'fix':fix})
			else : 
				raise Http404
		else :
			raise Http404	

class listFixtures(ListView):
	template_name = 'fixtures/listFixtures.html'
	model = Fixture
	context_object_name = 'fixtures' # Nombre de la lista a recorrer desde listFixtures.html	
	
	def get_queryset(self):
        #publisher = get_object_or_404(Publisher, name__iexact=self.args[0])
	        return Fixture.objects.filter(tournament=Tournament.objects.filter(complex=Complex.objects.filter(user=self.request.user)))

class deleteFixture(DeleteView):
	model = Fixture
	success_url = '/fixtures'
	template_name_suffix = '_confirm_delete' # This is: modelName_update_form.html
	form_class = FixtureForm
  	def get_form_kwargs(self):
		  	kwargs = super(deleteFixture, self).get_form_kwargs()
		  	kwargs.update({'user': self.request.user})
		  	return kwargs


	@method_decorator(login_required)
  	def dispatch(self, *args, **kwargs):
    		return super(deleteFixture, self).dispatch(*args, **kwargs)


  	def get_object(self, queryset=None):
    		fixture = super(deleteFixture, self).get_object()
    		torneo = Tournament.objects.get(id = fixture.tournament_id)
    		complejo = Complex.objects.get(id=torneo.complex_id)
    		usuario = UserProfile.objects.get(user_id =complejo.user_id)
    		if not usuario.user == self.request.user:
		        raise Http404
    		return fixture 		


class updateFixture(UpdateView):
	model = Fixture
	template_name_suffix = '_update_form' # This is: modelName_update_form.html
	success_url = '/fixtures'
	form_class = FixtureForm
  	def get_form_kwargs(self):
		  	kwargs = super(updateFixture, self).get_form_kwargs()
		  	kwargs.update({'user': self.request.user})
		  	return kwargs


	@method_decorator(login_required)
  	def dispatch(self, *args, **kwargs):
    		return super(updateFixture, self).dispatch(*args, **kwargs)

  	def get_object(self, queryset=None):
    		fixture = super(updateFixture, self).get_object()
    		torneo = Tournament.objects.get(id = fixture.tournament_id)
    		complejo = Complex.objects.get(id=torneo.complex_id)
    		usuario = UserProfile.objects.get(user_id =complejo.user_id)
    		if not usuario.user == self.request.user:
		        raise Http404
    		return fixture 	

def searchFixtures(request):
	#Class.objects.filter(date=datetime(2008,9,4)).query.as_sql()
  query = request.GET.get('q', '')
  if query:
	qset = (Q(date=query))
	results = Fixture.objects.filter(qset)

  else:
	results = []
  return render_to_response("fixtures/searchFixture.html",{"results": results,"query": query})	