#from django.shortcuts import render
from django.db.models import Q
from django.shortcuts import render_to_response
from models import Complex , User
from proyectoFinal.users.models import UserProfile
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from forms import ComplexForm
from django.http import HttpResponseRedirect
from django.views.generic import ListView, UpdateView, DeleteView
from django.core.context_processors import csrf # to increase security in the page
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import Http404

class listComplex(ListView):
	template_name = 'complexes/listComplexes.html'
	model = Complex
	context_object_name = 'complexes' # Nombre de la lista a recorrer desde listComplexes.html


def search_complex(request):
  query = request.GET.get('q', '')
  if query:
	qset = (Q(name__icontains=query))
	results = Complex.objects.filter(qset).distinct()

  else:
	results = []
  return render_to_response("complexes/searchComplex.html",{"results": results,"query": query})


class deleteComplex(DeleteView):
  model = Complex
  success_url = '/complexes'
  def get_form_kwargs(self):
  	kwargs = super(deleteComplex, self).get_form_kwargs()
  	#kwargs.update({'user': self.request.user})
  	return kwargs


  @method_decorator(login_required)
  def dispatch(self, *args, **kwargs):
    return super(deleteComplex, self).dispatch(*args, **kwargs)

  def get_object(self, queryset=None):
    #select the court object that we want to update
    complejo = super(deleteComplex, self).get_object()
    #select the user in base of the complex
    usuario = UserProfile.objects.get(user_id = complejo.user_id)
    if not usuario.user == self.request.user and usuario.userType == 'PR':
        raise Http404
    return complejo     
  

def register(request):
	if request.POST:
		cform = ComplexForm(request.POST) #create a UserForm
		
		#tform = TelephoneForm(request.POST)
		if cform.is_valid() : #if the information in the form its correct
		  
		  
		  
		  add=cform.save()
		  add2=Complex.objects.get(id=add.id)
		  #aqui se deberia reemplazar el 1 por el numero de id del usuario logueado
		  ident = UserProfile.objects.get(id = request.user.id)
		  add2.user_id = ident.id
		  add2.save()
		  return HttpResponseRedirect('/complexes')

	else:
		cform = ComplexForm()
		#tform = TelephoneForm()
	args = {}
	args.update(csrf(request))
	args['cform'] = cform
	return render_to_response('complexes/register.html', args)

def updatecomplexes(request):
	complexes = Complex.objects.filter(user = request.user.id)
	return render_to_response('complexes/updateAnyComplexes.html',{'complexes': complexes})

def deletecomplexes(request):
	complexes = Complex.objects.filter(user = request.user.id)
	return render_to_response('complexes/deleteAnyComplexes.html',{'complexes': complexes})	


class updateComplex(UpdateView):
  model = Complex
  fields = ['name','streetAddress','roaster','buffet','lockerRoom']
  template_name_suffix = '_update_complex'
  success_url = '/complexes' #redirect when the edit form is filled

  def get_form_kwargs(self):
  	kwargs = super(updateComplex, self).get_form_kwargs()
  	#kwargs.update({'user': self.request.user})
  	return kwargs


  @method_decorator(login_required)
  def dispatch(self, *args, **kwargs):
    return super(updateComplex, self).dispatch(*args, **kwargs)

  def get_object(self, queryset=None):
    #select the court object that we want to update
    complejo = super(updateComplex, self).get_object()
    #select the user in base of the complex
    usuario = UserProfile.objects.get(user_id = complejo.user_id)
    if not usuario.user == self.request.user and usuario.userType == 'PR':
        raise Http404
    return complejo    





