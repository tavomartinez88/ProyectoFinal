from django.db.models import Q
from django.shortcuts import render_to_response
from models import Fixture

from django.http import HttpResponseRedirect
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.core.context_processors import csrf # to increase security in the page
from django.template import RequestContext
from django.contrib import admin

class FixtureCreate(CreateView):
	model = Fixture
	success_url = '/fixtures'

class listFixtures(ListView):
	template_name = 'fixtures/listFixtures.html'
	model = Fixture
	context_object_name = 'fixtures' # Nombre de la lista a recorrer desde listFixtures.html	

class deleteFixture(DeleteView):
	model = Fixture
	success_url = '/fixtures'

class updateFixture(UpdateView):
	model = Fixture
	template_name_suffix = '_update_form' # This is: modelName_update_form.html
	success_url = '/fixtures'

def searchFixtures(request):
	#Class.objects.filter(date=datetime(2008,9,4)).query.as_sql()
  query = request.GET.get('q', '')
  if query:
	qset = (Q(date=query))
	results = Fixture.objects.filter(qset)

  else:
	results = []
  return render_to_response("fixtures/searchFixture.html",{"results": results,"query": query})	