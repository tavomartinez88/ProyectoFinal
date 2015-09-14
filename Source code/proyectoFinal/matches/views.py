#encoding:utf-8
from django.db.models import Q
from django.shortcuts import render_to_response
from models import Team , Match , Fixture
from proyectoFinal.tournaments.models import Tournament
from proyectoFinal.complexes.models import Complex
from forms import MatchForm, MatchFormUpdate
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.core.context_processors import csrf # to increase security in the page
from django.template import RequestContext
from django.contrib import admin
from proyectoFinal.users.models import UserProfile
from proyectoFinal.publicities.models import Publicity
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import Http404
from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy

"""
Esta vista se encarga de la creacion de un partido para ello el usuario debe estar identificado
y debe tener permisos de usuario propietario
"""
def addmatch(request,idfixture):
	try:
		usuario = UserProfile.objects.get(user=request.user)
	except Exception:
		usuario = None
	if request.user.is_anonymous():
		return HttpResponseRedirect('/login')
	if usuario.userType=='PR':
		try:
			publish_one = Publicity.objects.all().order_by('?').first()
		except Exception:
			publish_one = False
		try:
			publish_second = Publicity.objects.all().exclude(id=publish_one.id).order_by('?').last()
		except Exception:
			publish_second = False			
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
				try:
					f = Fixture.objects.get(id=idfixture)
				except Exception, e:
					message = """
							  Oops!!!, ha ocurrido un inconveniente, el fixture al que intenta agregar un 
							  partido aún no ha sido creado.Si el inconveniente persiste contactese.
							  """
					sendmail = True
					return render_to_response('404.html',{'message':message,'sendmail':sendmail})
				if mform.cleaned_data['day']<f.date and mform.cleaned_data['teamlocal']!=mform.cleaned_data['teamVisitant']:
					mform = MatchForm()
					fixture_id = Fixture.objects.get(id=idfixture)
					message_day_incorrect = "La fecha debe ser mayor o igual a "+str(object=f.date)
					return render_to_response('matches/addmatch.html', {'publish_one':publish_one,'publish_second':publish_second,'mform': mform, 'fixture_id':fixture_id,'message_day_incorrect':message_day_incorrect}, RequestContext(request, {}))
				if mform.cleaned_data['teamlocal']==mform.cleaned_data['teamVisitant'] and mform.cleaned_data['day']>=f.date:
					mform = MatchForm()
					fixture_id = Fixture.objects.get(id=idfixture)
					message_teams_incorrect = "el equipo local no pude ser igual que el visitante"
					return render_to_response('matches/addmatch.html', {'publish_one':publish_one,'publish_second':publish_second,'mform': mform, 'fixture_id':fixture_id,'message_teams_incorrect':message_teams_incorrect}, RequestContext(request, {}))
				    
				if mform.cleaned_data['teamlocal']==mform.cleaned_data['teamVisitant'] and mform.cleaned_data['day']<f.date:
					mform = MatchForm()
					fixture_id = Fixture.objects.get(id=idfixture)
					message_teams_incorrect = "el equipo local no pude ser igual que el visitante"
					message_day_incorrect = "La fecha debe ser mayor o igual a "+str(object=f.date)
					return render_to_response('matches/addmatch.html', {'publish_one':publish_one,'publish_second':publish_second,'mform': mform, 'fixture_id':fixture_id,'message_teams_incorrect':message_teams_incorrect, 'message_day_incorrect':message_day_incorrect}, RequestContext(request, {}))
				if usuario.userType == 'PR':
					match.save()
			else:
				return HttpResponseRedirect('/addmatch/'+str(object=idfixture))
			return HttpResponseRedirect('/fixtures')
		else:
			mform = MatchForm()		
			#la sig variable y el if verifica si el fixture es propiedad del usuario logueado
			verify_fixture = Fixture.objects.filter(id=idfixture ,tournament=Tournament.objects.filter(complex=Complex.objects.filter(user=request.user))).count()	
			if verify_fixture == 0:
				message = """
						  Oops!!!, ha ocurrido un inconveniente, el fixture al que intenta agregar un 
						  partido aún no ha sido creado.Si el inconveniente persiste contactese.
						  """
				sendmail = True
				return render_to_response('404.html',{'message':message,'sendmail':sendmail})
			else:
				fixture_id = Fixture.objects.get(id=idfixture)
			
		return render_to_response('matches/addmatch.html', {'publish_one':publish_one,'publish_second':publish_second,'mform': mform, 'fixture_id':fixture_id}, RequestContext(request, {}))
	else:
		message = '''Oops, ha ocurrido un inconveniente, no tienes los permisos suficientes para crear partidos, 
					 intente mas tarde, si aún persiste el inconveniente contactese.'''
		sendmail = True
		return render_to_response('404.html',{'message':message,'sendmail':sendmail})

"""
Esta vista se encarga de la eliminación de un partido para ello el usuario debe estar identificado
y debe tener permisos de usuario propietario
"""
class deleteMatch(DeleteView):
	model = Match
	success_url = '/matches'

  	def get_form_kwargs(self):
  		kwargs = super(deleteMatch, self).get_form_kwargs()
  		return kwargs

  	def get_success_url(self):
  		objeto_match_current = self.kwargs['pk']
  		id_match = int(x=objeto_match_current)
  		match_current = Match.objects.get(id=id_match)
  		fixture_current = Fixture.objects.get(id = match_current.fixture_id)
  		return reverse('list_matches', kwargs={'idfixture': fixture_current.id})  		


	
  	def dispatch(self, *args, **kwargs):
  		if self.request.user.is_anonymous():
  			return HttpResponseRedirect('/login')
  		else:
  			try:
  				usuario = UserProfile.objects.get(user=self.request.user)
  				if usuario.userType=='CM':
  					message = """
  							  Oops!!! ha ocurrido un inconveniente,no tienes los permisos necesarios
  							  para eliminar este partido, intenta más tarde.Si aún persiste el inconveniente
  							  contactanos.
  							  """
  					sendmail = True
  					return render_to_response('404.html',{'message':message,'sendmail':sendmail})
  				else:
  					return super(deleteMatch, self).dispatch(*args, **kwargs)
  			except Exception, e:
  				return HttpResponseRedirect('/login')

  	def get_object(self, queryset=None):
	    #select the court object that we want to update
	    partido = super(deleteMatch, self).get_object()
	    #select the user in base of the complex
	    fixture = Fixture.objects.get(id=partido.fixture.id)
	    torneo = Tournament.objects.get(id=fixture.tournament_id)
	    complejo = Complex.objects.get(id=torneo.complex_id)
	    usuario = UserProfile.objects.get(user_id = complejo.user_id)
	    if not usuario.user == self.request.user and usuario.userType == 'PR':
	        message = """
	        		  Oops!!! ha ocurrido un inconveniente,no tienes los permisos necesarios
	        		  para eliminar este partido, intenta más tarde.Si aún persiste el inconveniente
	        		  contactanos.
	        		  """
	        sendmail = True
	        return render_to_response('404.html',{'message':message,'sendmail':sendmail})
	    return partido

	def get_context_data(self, **kwargs):
	    # Call the base implementation first to get a context
	    context = super(deleteMatch, self).get_context_data(**kwargs)
	    # Add in the publisher
	    try:
	    	context['publish_one'] = Publicity.objects.all().order_by('?').first()
	    except Exception:
	    	context['publish_one'] = False
	    try:
	    	context['publish_second'] = Publicity.objects.all().exclude(id=context['publish_one'].id).order_by('?').first()
	    except Exception:
	    	context['publish_second'] = False
	    return context	    

"""
Esta vista se encarga de actualizar el resultado de un partido, para ello el usuario debe estar identificado 
o logueado y ademas debe tener permisos de usuario propietario
"""
class addResult(UpdateView):
	model = Match
	fields = ['scoreLocal','scoreVisit']
	template_name_suffix = '_update_form' # This is: modelName_update_form.html
	form_class = MatchFormUpdate

  	def get_form_kwargs(self):
  		kwargs = super(addResult, self).get_form_kwargs()
  		return kwargs

  	def get_success_url(self):
  		objeto_match_current = self.kwargs['pk']
  		id_match = int(x=objeto_match_current)
  		match_current = Match.objects.get(id=id_match)
  		fixture_current = Fixture.objects.get(id = match_current.fixture_id)
  		return reverse('list_matches', kwargs={'idfixture': fixture_current.id})

	
  	def dispatch(self, *args, **kwargs):
  		if self.request.user.is_anonymous():
  			return HttpResponseRedirect('/login')
  		else:
  			try:
  				usuario = UserProfile.objects.get(user=self.request.user)
  				if usuario.userType=='CM':
  					message = """
  							  Oops!!! ha ocurrido un inconveniente,no tienes los permisos necesarios
  							  para modificar el resultado de  este partido, intenta más tarde.Si aún persiste el inconveniente
  							  contactanos.
  							  """
  					sendmail = True
  					return render_to_response('404.html',{'message':message,'sendmail':sendmail})
  				else:
  					return super(deleteMatch, self).dispatch(*args, **kwargs)
  			except Exception, e:
  				return HttpResponseRedirect('/login')

  	def get_object(self, queryset=None):
	    #select the court object that we want to update
	    partido = super(addResult, self).get_object()
	    #select the user in base of the complex
	    fixture = Fixture.objects.get(id=partido.fixture.id)
	    torneo = Tournament.objects.get(id=fixture.tournament_id)
	    complejo = Complex.objects.get(id=torneo.complex_id)
	    usuario = UserProfile.objects.get(user_id = complejo.user_id)
	    if not usuario.user == self.request.user and usuario.userType == 'PR':
	        message = """
	        		  Oops!!! ha ocurrido un inconveniente,no tienes los permisos necesarios
	        		  para eliminar este partido, intenta más tarde.Si aún persiste el inconveniente
	        		  contactanos.
	        		  """
	        sendmail = True
	        return render_to_response('404.html',{'message':message,'sendmail':sendmail})
	    return partido	

	def get_context_data(self, **kwargs):
	    # Call the base implementation first to get a context
	    context = super(addResult, self).get_context_data(**kwargs)
	    # Add in the publisher
	    try:
	    	context['publish_one'] = Publicity.objects.all().order_by('?').first()
	    except Exception:
	    	context['publish_one'] = False
	    try:
	    	context['publish_second'] = Publicity.objects.all().exclude(id=context['publish_one'].id).order_by('?').first()
	    except Exception:
	    	context['publish_second'] = False
	    return context	    

"""
Esta vista se encarga de la busqueda de partidos
"""
def searchMatch(request):
	
  query = request.GET.get('q', '')
  if query:
  	try:
		qset = (Q(day=query))
		results = Match.objects.filter(qset)
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
  return render_to_response("matches/searchMatch.html",{"results": results,"query": query,'publish_one':publish_one,'publish_second':publish_second}, RequestContext(request, {}))		

"""
Esta vista se encarga de listar los partidos correspondientes a un fixture siempre y cuando 
el usuario este identificado
"""
def listMatchForFixture(request,idfixture):
	if request.user.is_anonymous():
		raise Http404
	try:
		publish_one = Publicity.objects.all().order_by('?').first()
	except Exception:
		publish_one = False
	try:
		publish_second = Publicity.objects.all().exclude(id=publish_one.id).order_by('?').last()
	except Exception:
		publish_second = False		
	try:
		fix = Fixture.objects.get(id=idfixture)
		partidos = Match.objects.filter(fixture_id=fix.id)
		return render_to_response('matches/listMatchForFixture.html', {'publish_one':publish_one,'publish_second':publish_second,'partidos': partidos, 'fix':fix}, RequestContext(request, {}))
	except Exception:
	    message = """
	    		  Oops!!! ha ocurrido un inconveniente,intenta más tarde.Si aún persiste el inconveniente
	    		  contactanos.
	    		  """
	    sendmail = True
	    return render_to_response('404.html',{'message':message,'sendmail':sendmail})
