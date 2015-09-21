#encoding:utf-8
from django.db.models import Q
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.core.context_processors import csrf # to increase security in the site
from django.template import RequestContext
from models import Tournament
from forms import TournamentForm, TournamentFormUpdate
from proyectoFinal.fixtures.models import Fixture
from proyectoFinal.publicities.models import Publicity
from proyectoFinal.users.models import UserProfile
from proyectoFinal.complexes.models import Complex
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import Http404

"""
Esta vista se encarga de la ceación de un torneo siempre y cuando el usuario este logueado,
dicho usuario también debe tener permisos de usuario propietario
"""
class TournamentCreate(CreateView):
	model = Tournament
	success_url = '/newfixture'
	form_class = TournamentForm

	def get_form_kwargs(self):
    		kwargs = super(TournamentCreate, self).get_form_kwargs()
    		kwargs.update({'user': self.request.user})
    		return kwargs

	def get_context_data(self, **kwargs):
	    # Call the base implementation first to get a context
	    context = super(TournamentCreate, self).get_context_data(**kwargs)
	    # Add in the publisher
	    try:
	    	context['publish_one'] = Publicity.objects.all().order_by('?').first()
	    except Exception:
	    	context['publish_one'] = False
	    try:
	    	context['publish_second'] = Publicity.objects.all().exclude(id=context['publish_one'].id).first()
	    except Exception:
	    	context['publish_second'] = False
	    return context	    		

   	def dispatch(self, *args, **kwargs):
   		try:
   			usuario = UserProfile.objects.get(user=self.request.user)
  		except Exception:
   			return HttpResponseRedirect('/login')
   		if usuario.userType=='PR':
   			return super(TournamentCreate, self).dispatch(*args, **kwargs)
   		else:
		   	message = """
		   			  Oops!!! ha ocurrido un inconveniente,no tienes los permisos necesarios para 
		   			  poder crear un torneo.Para mas información contactese.
		   			  """
		   	sendmail = True		  
		   	return render_to_response('404.html',{'message':message,'sendmail':sendmail})
    		

"""
Esta vista se encarga de listar los torneos.Si el usuario no esta logueado o si el usuario logueado
es un usuario con permisos de usuario comun mostrará todos los torneos.
En el caso de que sea un usuario con permisos de usuario propietario mostrará solo aquellos torneos que 
se disputan en complejos de su propiedad
"""
class listTournaments(ListView):
	template_name = 'tournaments/listTournaments.html'
	model = Tournament
	context_object_name = 'tournaments' # Nombre de la lista a recorrer desde listReservations.html
	paginate_by = 6

	def get_queryset(self):
		if self.request.user.is_anonymous():
			return Tournament.objects.all()
		else:
			try:
				usuario = UserProfile.objects.get(user = self.request.user)
			except Exception:
				usuario = None
			if usuario.userType=='CM':
				return Tournament.objects.all()
			else:
				return Tournament.objects.filter(complex=Complex.objects.filter(user=self.request.user))

	def get_context_data(self, **kwargs):
	    # Call the base implementation first to get a context
	    context = super(listTournaments, self).get_context_data(**kwargs)
	    # Add in the publisher
	    try:
	    	context['publish_one'] = Publicity.objects.all().order_by('?').first()
	    except Exception:
	    	context['publish_one'] = False
	    try:
	    	context['publish_second'] = Publicity.objects.all().exclude(id=context['publish_one'].id).first()
	    except Exception:
	    	context['publish_second'] = False
	    try:
	    	context['publish_third'] = Publicity.objects.all().order_by('?').exclude(id=context['publish_one'].id).exclude(id=context['publish_second'].id).first()
	    except Exception:
	    	context['publish_third'] = False  	
	    return context			


"""
Esta vista se encarga de obtener los equipos inscriptos a un determinado torneo
"""
def teamsinscriptions(request,idtournament):
  try:
  	torneo = Tournament.objects.get(id = idtournament)
  except Exception:
  	torneo = None
  try:
	publish_one = Publicity.objects.all().order_by('?').first()
  except Exception:
	publish_one = False
  try:
	publish_second = Publicity.objects.all().exclude(id=publish_one.id).order_by('?').first()
  except Exception:
  	publish_second = False
  try:
	publish_third = Publicity.objects.all().exclude(id=publish_one.id).exclude(id=publish_second.id).order_by('?').first()
  except Exception:
  	publish_third = False  	
  return render_to_response("tournaments/teamsinscriptions.html",{"torneo": torneo,'publish_one':publish_one,'publish_second':publish_second,'publish_third':publish_third}, RequestContext(request, {}))

"""
Esta vista se encarga de actualizar un torneo donde el usuario debe estar logueado y ademas debe 
tener permisos de usuario propietario
"""
class markAsFinished(UpdateView):
	model = Tournament
	template_name_suffix = '_update_form' # This is: modelName_update_form.html
	success_url = '/tournaments'
	form_class = TournamentFormUpdate


   	def dispatch(self, *args, **kwargs):
   		if self.request.user.is_anonymous():
   			return HttpResponseRedirect('/login')
   		try:
   			usuario = UserProfile.objects.get(user = self.request.user)
   		except Exception:
   			usuario = None
   		if usuario.userType=='PR':
   			return super(markAsFinished, self).dispatch(*args, **kwargs)
   		else:
		   	message = """
		   			  Oops!!! ha ocurrido un inconveniente,no tienes los permisos necesarios para 
		   			  poder dar finalización este torneo.Para más información contactese.
		   			  """
		   	sendmail = True		  
		   	return render_to_response('404.html',{'message':message,'sendmail':sendmail}, RequestContext(self.request, {}))

	def get_context_data(self, **kwargs):
	    # Call the base implementation first to get a context
	    context = super(markAsFinished, self).get_context_data(**kwargs)
	    # Add in the publisher
	    try:
	    	context['publish_one'] = Publicity.objects.all().order_by('?').first()
	    except Exception:
	    	context['publish_one'] = False
	    try:
	    	context['publish_second'] = Publicity.objects.all().exclude(id=context['publish_one'].id).first()
	    except Exception:
	    	context['publish_second'] = False 	
	    return context	    			
   		

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

"""
Esta vista se encarga de eliminar un torneo donde el usuario debe estar logueado y ademas debe 
tener permisos de usuario propietario
"""
class cancelTournament(DeleteView):
	model = Tournament
	success_url = '/tournaments'

   	def get_object(self, queryset=None):
		tournament = super(cancelTournament,self).get_object()
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

	def get_context_data(self, **kwargs):
	    # Call the base implementation first to get a context
	    context = super(cancelTournament, self).get_context_data(**kwargs)
	    # Add in the publisher
	    try:
	    	context['publish_one'] = Publicity.objects.all().order_by('?').first()
	    except Exception:
	    	context['publish_one'] = False
	    try:
	    	context['publish_second'] = Publicity.objects.all().exclude(id=context['publish_one'].id).first()
	    except Exception:
	    	context['publish_second'] = False  	
	    return context	     	

	#restricted area for anonymous users
	#@method_decorator(login_required)
    	def dispatch(self, *args, **kwargs):
    		try:
    			usuario = UserProfile.objects.get(user=self.request.user)
    		except Exception:
    			return HttpResponseRedirect('/login')
    		if usuario.userType=='PR':
    			return super(cancelTournament, self).dispatch(*args, **kwargs)
    		else:
	   			message = """
			   			  Oops!!! ha ocurrido un inconveniente,no tienes los permisos necesarios para 
			   			  poder cancelar este torneo.Para más información contactese.
			   			  """
			   	sendmail = True		  
			   	return render_to_response('404.html',{'message':message,'sendmail':sendmail},RequestContext(self.request, {}))
    		

"""
Esta vista se encarga de buscar torneos
"""
def searchTournament(request):
  query = request.GET.get('q', '')
  if query:
  	try:
		qset = (Q(name__icontains=query))
		results = Tournament.objects.filter(qset).distinct()
  	except Exception:
  		raise Http404
  else:
	results = []
  try:
   	publish_one = Publicity.objects.all().order_by('?').first()
  except Exception:
   	publish_one = False
  try:
  	publish_second = Publicity.objects.all().exclude(id=publish_one.id).first()
  except Exception:
   	publish_second = False
  return render_to_response("tournaments/searchTournament.html",{"results": results,"query": query,'publish_one':publish_one,'publish_second':publish_second},RequestContext(request, {}))