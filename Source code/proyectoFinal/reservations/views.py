from django.db.models import Q
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.core.context_processors import csrf # to increase security in the site
from django.template import RequestContext
from models import Reservation
from models import Court
from proyectoFinal.users.models import UserProfile
from proyectoFinal.complexes.models import Complex
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import Http404

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


	def get_queryset(self):
		if self.request.user.is_anonymous():
			raise Http404
		else:
			usuario = UserProfile.objects.get(user=self.request.user)
			if usuario.userType=='CM':
				return Reservation.objects.filter(user_id=self.request.user)
			else:
				return Reservation.objects.filter(court=Court.objects.filter(complex=Complex.objects.filter(user=self.request.user)))
			
			

@login_required
def updatereservations(request):
	usuario = UserProfile.objects.get(user=request.user)
	complejo = Complex.objects.filter(user=request.user)
	court = Court.objects.filter(complex=Complex.objects.filter(user=request.user))
	if usuario.userType=='CM':
		reservations = Reservation.objects.filter(user_id=request.user.id, attended = False)
	else:
		reservations = Reservation.objects.filter(court=court, attended = False)			
	return render_to_response('reservations/updateAnyReservations.html',{'complejo': complejo,"reservations": reservations})

@login_required
def deletereservations(request):
	usuario = UserProfile.objects.get(user=request.user)
	complejo = Complex.objects.filter(user=request.user)
	court = Court.objects.filter(complex=Complex.objects.filter(user=request.user))
	if usuario.userType=='CM':
		reservations = Reservation.objects.filter(user_id=request.user.id, attended = False)
	else:
		reservations = Reservation.objects.filter(court=court, attended = False)	
	return render_to_response('reservations/deleteAnyReservations.html',{'complejo': complejo,'reservations':reservations})
		
class markAsAttended(UpdateView):
	model = Reservation
	#fields = ['attended']
	template_name_suffix = '_update_form' # This is: modelName_update_form.html
	success_url = '/reservations'

	#restricted area for anonymous users
	@method_decorator(login_required)
    	def dispatch(self, *args, **kwargs):
    	    return super(markAsAttended, self).dispatch(*args, **kwargs)
   	
   	def get_object(self,queryset=None):
   		reserva = super(markAsAttended, self).get_object()
   		usuario = UserProfile.objects.get(user=self.request.user)
   		if usuario.userType=='CM':
   			if (reserva.user != self.request.user):
   				raise Http404
   			return reserva
   		else:
   			res = Reservation.objects.filter(id=reserva.id,court=Court.objects.filter(complex=Complex.objects.filter(user=self.request.user))).count()
			if res<1:
				raise Http404
			else:
				reserva = Reservation.objects.get(id=reserva.id,court=Court.objects.filter(complex=Complex.objects.filter(user=self.request.user)))
				return reserva    	    

class cancelReservation(DeleteView):
	model = Reservation
	success_url = '/reservations'

	#restricted area for anonymous users
	@method_decorator(login_required)
    	def dispatch(self, *args, **kwargs):
    	    return super(cancelReservation, self).dispatch(*args, **kwargs)

   	def get_object(self,queryset=None):
   		reserva = super(cancelReservation, self).get_object()
   		usuario = UserProfile.objects.get(user=self.request.user)
   		if usuario.userType=='CM':
   			if (reserva.user != self.request.user):
   				raise Http404
   			return reserva
   		else:
   			res = Reservation.objects.filter(id=reserva.id,court=Court.objects.filter(complex=Complex.objects.filter(user=self.request.user))).count()
			if res<1:
				raise Http404
			else:
				reserva = Reservation.objects.get(id=reserva.id,court=Court.objects.filter(complex=Complex.objects.filter(user=self.request.user)))
				return reserva
			
   		


@login_required
def searchReservation(request):
	#Class.objects.filter(date=datetime(2008,9,4)).query.as_sql()
  query = request.GET.get('q', '')
  usuario = UserProfile.objects.get(user=request.user)
  if usuario.userType=='CM':
  	if query:
  		try:
  			qset = (Q(date=query))
			results = Reservation.objects.filter(qset)
  		except Exception:
  			raise Http404
	else:
		results = []
  	return render_to_response("reservations/searchReservation.html",{"results": results,"query": query})
  else:
  	if query:
  		try:
  			qset = (Q(date=query))
			results = Reservation.objects.filter(qset,court=Court.objects.filter(complex=Complex.objects.filter(user=request.user)))
  		except Exception:
  			raise Http404
		
	else:
		results = []
  	return render_to_response("reservations/searchReservation.html",{"results": results,"query": query})
  