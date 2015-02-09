from django.db.models import Q
from django.shortcuts import render_to_response
from models import Court
from forms import CourtForm
from django.http import HttpResponseRedirect
from django.views.generic import ListView, UpdateView, DeleteView
from django.core.context_processors import csrf # to increase security in the page
from django.template import RequestContext

def register(request):
	if request.POST:
		form = CourtForm(request.POST) #create a UserForm
		
		if form.is_valid(): #if the information in the form its correct
						
			form.save() #save the user model
			return HttpResponseRedirect('/courts')
	else:
		form = CourtForm()
		
	return render_to_response('courts/register.html', {'form': form}, RequestContext(request, {}))

class listCourt(ListView):
	template_name = 'courts/listCourts.html'
	model = Court
	context_object_name = 'courts' # Nombre de la lista a recorrer desde listUsers.html


class updateCourt(UpdateView):
  model = Court
  #fields = ['name','streetAddress','roaster','buffet','lockerRoom']
  template_name_suffix = '_update_court'
  success_url = '/courts' #redirect when the edit form is filled


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

# Create your views here.
