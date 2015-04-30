from django.db.models import Q
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.core.context_processors import csrf # to increase security in the site
from django.template import RequestContext
from models import Reservation
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class ReservationCreate(CreateView):
	model = Reservation
	fields = ['date', 'hour', 'minutes', 'court']
	success_url = '/reservations'

	#restricted area for anonymous users
	@method_decorator(login_required)
    	def dispatch(self, *args, **kwargs):
    	    return super(ReservationCreate, self).dispatch(*args, **kwargs)

	#set the user that's logged in as the user that make the reservation
	def form_valid(self, form):
    		form.instance.user = self.request.user
    		return super(ReservationCreate, self).form_valid(form)

class listReservations(ListView):
	template_name = 'reservations/listReservations.html'
	model = Reservation
	context_object_name = 'reservations' # Nombre de la lista a recorrer desde listReservations.html

class markAsAttended(UpdateView):
	model = Reservation
	fields = ['attended']
	template_name_suffix = '_update_form' # This is: modelName_update_form.html
	success_url = '/reservations'

class cancelReservation(DeleteView):
	model = Reservation
	success_url = '/reservations'

def searchReservation(request):
	#Class.objects.filter(date=datetime(2008,9,4)).query.as_sql()
  query = request.GET.get('q', '')
  if query:
	qset = (Q(date=query))
	results = Reservation.objects.filter(qset)

  else:
	results = []
  return render_to_response("reservations/searchReservation.html",{"results": results,"query": query})