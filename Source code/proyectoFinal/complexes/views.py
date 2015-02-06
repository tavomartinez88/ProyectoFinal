#from django.shortcuts import render
from django.db.models import Q
from django.shortcuts import render_to_response
from models import Complex , User
from forms import ComplexForm
from django.http import HttpResponseRedirect
from django.views.generic import ListView, UpdateView, DeleteView
from django.core.context_processors import csrf # to increase security in the page

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
  

def register(request):
	if request.POST:
		cform = ComplexForm(request.POST) #create a UserForm
		
		#tform = TelephoneForm(request.POST)
		if cform.is_valid() : #if the information in the form its correct
		  
		  
		  
		  add=cform.save()
		  add2=Complex.objects.get(id=add.id)
		  #aqui se deberia reemplazar el 1 por el numero de id del usuario logueado
		  ident = User.objects.get(id=1)
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


class updateComplex(UpdateView):
  model = Complex
  fields = ['name','streetAddress','roaster','buffet','lockerRoom']
  template_name_suffix = '_update_complex'
  success_url = '/complexes' #redirect when the edit form is filled



# Create your views here.

