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
from forms import ReservationForm


@login_required
def reservationCreate(request):
	usuario = UserProfile.objects.get(user=request.user)
	if usuario.userType=='CM':
		return HttpResponseRedirect('/addreservationCommonUser')
	else:
		return HttpResponseRedirect('/addreservationOwnerUser')
	

class CreateReservationAsCommonUser(CreateView):
	model = Reservation
	fields = ['date', 'hour', 'minutes', 'court']
	success_url = '/reservations'
	
	#restricted area for anonymous users
	@method_decorator(login_required)
    	def dispatch(self, *args, **kwargs):
    		usuario = UserProfile.objects.get(user=self.request.user)
    		if usuario.userType=='CM':
    			return super(CreateReservationAsCommonUser, self).dispatch(*args, **kwargs)
    		else:
    			raise Http404
    		

	#set the user that's logged in as the user that make the reservation
	def form_valid(self, form):
			user_logued = UserProfile.objects.get(user=self.request.user)
			form.instance.user = user_logued
			reservas = Reservation.objects.filter(date=form.instance.date,hour=form.instance.hour,minutes=form.instance.minutes,court=form.instance.court).count()
			print reservas
			if reservas == 0:
				return super(CreateReservationAsCommonUser, self).form_valid(form)
			else:
				raise Http404


class CreateReservationAsOwnerUser(CreateView):
	model = Reservation
	fields = ['date', 'hour', 'minutes', 'user', 'court']
	success_url = '/reservations'
	form_class = ReservationForm
	
	#restricted area for anonymous users
	@method_decorator(login_required)
    	def dispatch(self, *args, **kwargs):
    		if usuario.userType=='PR':
    			return super(CreateReservationAsOwnerUser, self).dispatch(*args, **kwargs)
    		else:
    			raise Http404

	#set the user that's logged in as the user that make the reservation
	def form_valid(self, form):
			reservas = Reservation.objects.filter(date=form.instance.date,hour=form.instance.hour,minutes=form.instance.minutes,court=form.instance.court).count()
			print reservas
			if reservas == 0:
				return super(CreateReservationAsOwnerUser, self).form_valid(form)
			else:
				raise Http404
	
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
				return Reservation.objects.filter(user_id=UserProfile.objects.get(user=self.request.user))
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
  