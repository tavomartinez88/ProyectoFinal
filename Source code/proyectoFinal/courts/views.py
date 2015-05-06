from django.db.models import Q
from django.shortcuts import render_to_response
from models import Court
from models import Complex
from proyectoFinal.users.models import UserProfile
from forms import CourtForm
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.core.context_processors import csrf # to increase security in the page
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import Http404



class CreateCourt(CreateView):
	model = Court
	success_url = '/courts'
	form_class = CourtForm

	def get_form_kwargs(self):
    		kwargs = super(CreateCourt, self).get_form_kwargs()
    		kwargs.update({'user': self.request.user})
    		return kwargs

	#restricted area for anonymous users
	@method_decorator(login_required)
    	def dispatch(self, *args, **kwargs):
    	    return super(CreateCourt, self).dispatch(*args, **kwargs)


class listCourt(ListView):
	template_name = 'courts/listCourts.html'
	model = Court
	context_object_name = 'courts' # Nombre de la lista a recorrer desde listUsers.html


class updateCourt(UpdateView):
  model = Court
  #fields = ['name','streetAddress','roaster','buffet','lockerRoom']
  template_name_suffix = '_update_court'
  success_url = '/courts' #redirect when the edit form is filled
  

  def get_form_kwargs(self):
  	kwargs = super(updateCourt, self).get_form_kwargs()
  	#kwargs.update({'user': self.request.user})
  	return kwargs


  @method_decorator(login_required)
  def dispatch(self, *args, **kwargs):
    return super(updateCourt, self).dispatch(*args, **kwargs)

  def get_object(self, queryset=None):
    #select the court object that we want to update
    cancha = super(updateCourt, self).get_object()
    #select the complex in base of the court
    complejo = Complex.objects.get(id = cancha.complex_id)
    #select the user in base of the complex
    usuario = UserProfile.objects.get(user_id = complejo.user_id)
    if not usuario.user == self.request.user:
        raise Http404
    return cancha    




def search_court(request):
  query = request.GET.get('q', '')
  if query:
	qset = (Q(complejo__name__icontains=query))
	results = Court.objects.filter(qset).distinct()

  else:
	results = []
  return render_to_response("courts/searchCourt.html",{"results": results,"query": query})


class deleteCourt(DeleteView):
  model = Court
  success_url = '/courts'

  def get_form_kwargs(self):
  	kwargs = super(deleteCourt, self).get_form_kwargs()
  	#kwargs.update({'user': self.request.user})
  	return kwargs


  @method_decorator(login_required)
  def dispatch(self, *args, **kwargs):
    return super(deleteCourt, self).dispatch(*args, **kwargs)

  def get_object(self, queryset=None):
    #select the court object that we want to delete
    cancha = super(deleteCourt, self).get_object()
    #select the complex in base of the court
    complejo = Complex.objects.get(id = cancha.complex_id)
    #select the user in base of the complex
    usuario = UserProfile.objects.get(user_id = complejo.user_id)
    if not usuario.user == self.request.user:
        raise Http404
    return cancha    


# Create your views here.
