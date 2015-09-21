#encoding:utf-8
from django.db.models import Q
from django.shortcuts import render_to_response
from django.shortcuts import render
from models import Fixture
from proyectoFinal.matches.models import Match
from proyectoFinal.users.models import UserProfile
from proyectoFinal.tournaments.models import Tournament
from proyectoFinal.complexes.models import Complex
from proyectoFinal.publicities.models import Publicity
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.core.context_processors import csrf # to increase security in the page
from django.template import RequestContext
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import Http404
from forms import FixtureForm, FixtureFormUpdate
import datetime
from django.http import HttpResponse


"""
Esta vista se encarga de crear un fixture para lo cual el usuario debe estar logueado y ademas
dicho usuario debe tener permisos de usuario propietario
"""
class FixtureCreate(CreateView):
	model = Fixture
	success_url = '/fixtures'
	form_class = FixtureForm
	#restricted area for anonymous users
	#@method_decorator(login_required)
    	def dispatch(self, *args, **kwargs):
    		if self.request.user.is_anonymous():
    			return HttpResponseRedirect('/login')
    		try:
    			usuario = UserProfile.objects.get(user=self.request.user)
    		except Exception:
    			return HttpResponseRedirect('/login')
    		if usuario.userType=='PR':
    			return super(FixtureCreate, self).dispatch(*args, **kwargs)
    		else:
    			message = '''
    					  Oops!!! ha ocurrido un inconveniente, no cuentas con los permisos necesarios
    					  para crear fixtures.Si el problema persiste puedes contactarnos.
    					  '''
    			sendmail = True
    			return render_to_response('404.html',{'message':message,'sendmail':sendmail})

	def get_context_data(self, **kwargs):
	    # Call the base implementation first to get a context
	    context = super(FixtureCreate, self).get_context_data(**kwargs)
	    # Add in the publisher
	    try:
	    	context['publish_one'] = Publicity.objects.all().order_by('?').first()
	    except Exception:
	    	context['publish_one'] = False
	    try:
	    	context['publish_second'] = Publicity.objects.all().exclude(id=context['publish_one'].id).order_by('?').last()
	    except Exception:
	    	context['publish_second'] = False
	    return context    			
    		

	
	def form_valid(self, form):
    		form.instance.user = self.request.user
    		return super(FixtureCreate, self).form_valid(form)
	
	def get_form_kwargs(self):
    		kwargs = super(FixtureCreate, self).get_form_kwargs()
    		kwargs.update({'user': self.request.user})
    		return kwargs    		

"""
Esta vista carga todos los fixtures , solo podran visualizarse en caso de que el usuario se 
logueo o identifico
"""
class listFixtures(ListView):
	template_name = 'fixtures/listFixtures.html'
	model = Fixture
	context_object_name = 'fixtures'

	def dispatch(self, *args, **kwargs):
		if self.request.user.is_anonymous():
			return HttpResponseRedirect('/login')
		else:
			return super(listFixtures, self).dispatch(*args, **kwargs)
   	   	

	def get_context_data(self, **kwargs):
	    # Call the base implementation first to get a context
	    context = super(listFixtures, self).get_context_data(**kwargs)
	    # Add in the publisher
	    try:
	    	context['publish_one'] = Publicity.objects.all().order_by('?').first()
	    except Exception:
	    	context['publish_one'] = False
	    try:
	    	context['publish_second'] = Publicity.objects.all().exclude(id=context['publish_one'].id).order_by('?').last()
	    except Exception:
	    	context['publish_second'] = False
	    return context    			   	    

	def get_queryset(self):		
			try:
				usuario = UserProfile.objects.get(user=self.request.user)
			except Exception:
				usuario = None
			if usuario.userType=='PR':
				return Fixture.objects.filter(tournament=Tournament.objects.filter(complex=Complex.objects.filter(user=self.request.user)))
			else:
				return Fixture.objects.filter(tournament=Tournament.objects.filter(inProgress=True))
			
"""
Esta vista se encarga de la eliminacion de un fixture, para lo cual el usuario debe estar indentificado
o logueado y ademas tener permisos de usuario propietario
"""

def deleteFixture(request,idfixture):
	if request.user.is_anonymous():
		return HttpResponseRedirect('/login')
	else:
		try:
			usuario_logued = UserProfile.objects.get(user=request.user)
		except Exception:
			usuario_logued = None
		if usuario_logued.userType=='CM' :
			message = 'Oops!!! ha ocurrido un inconveniente, no cuentas con los permisos necesarios para eliminar este fixtures.Si el problema persiste puedes contactarnos.'
			sendmail = True
			return render_to_response('404.html',{'message':message,'sendmail':sendmail})		
		else:
			try:
				fixture = Fixture.objects.get(id=idfixture)
			except Exception:
				raise Http404

			if fixture.tournament.complex.user!=request.user:
				message = 'Oops!!! ha ocurrido un inconveniente,no eres el dueño de este fixture.Ante alguna duda contactese.'    			
				sendmail = True
				return render_to_response('404.html',{'message':message,'sendmail':sendmail})    			
			else:
				"""
				En lugar de eliminar simplemente el fixture, elimino el torneo y eso conlleva a la 
				eliminacion	del fixture..con esto consigo que no me queden torneos colgados, 
				es decir torneos sin fixtures.Esto se produce por la eliminacion de datos en cascada
				"""
				torneo = Tournament.objects.get(id=fixture.tournament.id)
				torneo.delete()
				return HttpResponseRedirect('/fixtures')
			
		
	


"""
Esta vista se encarga de la actualizacion de un fixture, para lo cual el usuario debe estar indentificado
o logueado y ademas tener permisos de usuario propietario
"""
class updateFixture(UpdateView):
	model = Fixture
	template_name_suffix = '_update_form' # This is: modelName_update_form.html
	success_url = '/fixtures'
	form_class = FixtureFormUpdate
  	def get_form_kwargs(self):
		  	kwargs = super(updateFixture, self).get_form_kwargs()
		  	kwargs.update({'user': self.request.user})
		  	return kwargs


	#@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		if self.request.user.is_anonymous():
			return HttpResponseRedirect('/login')
			print "te redirecciona del if del dispatch"
		else:
			try:
				user_logued = UserProfile.objects.get(user=self.request.user)
			except Exception:
				return HttpResponseRedirect('/login')

			if user_logued.userType=='CM':
  				message = ' Oops!!! ha ocurrido un inconveniente, no tienes los permisos necesarios para actualizar este fixture, intente más tarde.Si aún persiste el inconveniente contactese.'
  				sendmail = True
  				return render_to_response('404.html',{'message':message,'sendmail':sendmail})		    
			else:
				return super(updateFixture, self).dispatch(*args, **kwargs)
			
	def get_context_data(self, **kwargs):
	    # Call the base implementation first to get a context
	    context = super(updateFixture, self).get_context_data(**kwargs)
	    # Add in the publisher
	    try:
	    	context['publish_one'] = Publicity.objects.all().order_by('?').first()
	    except Exception:
	    	context['publish_one'] = False
	    try:
	    	context['publish_second'] = Publicity.objects.all().exclude(id=context['publish_one'].id).order_by('?').last()
	    except Exception:
	    	context['publish_second'] = False
	    return context    			 		

  	def get_object(self, queryset=None):
    		fixture = super(updateFixture, self).get_object()
    		torneo = Tournament.objects.get(id = fixture.tournament_id)
    		complejo = Complex.objects.get(id=torneo.complex_id)
    		usuario = UserProfile.objects.get(user_id =complejo.user_id)
    		if usuario.user != self.request.user:
    			raise Http404
    		return fixture  	


"""
Esta vista se encarga de la busqueda de fixtures
"""
def searchFixtures(request):
  query = request.GET.get('q', '')
  if query:
  	try:
  		qset = (Q(name__icontains=query))
		results = Fixture.objects.filter(qset)
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
  return render_to_response("fixtures/searchFixture.html",{"results": results,"query": query,'publish_one':publish_one,'publish_second':publish_second}, RequestContext(request, {}))