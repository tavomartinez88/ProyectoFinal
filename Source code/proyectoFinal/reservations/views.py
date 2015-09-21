#encoding:utf-8
from django.db.models import Q
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.core.context_processors import csrf # to increase security in the site
from django.template import RequestContext
from models import Reservation
from models import Court
from proyectoFinal.users.models import UserProfile
from proyectoFinal.publicities.models import Publicity
from proyectoFinal.complexes.models import Complex
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import Http404
from forms import ReservationFormCommonUser, ReservationFormOwnerUser
from django.http import HttpResponse
from datetime import datetime
from datetime import date
from django.shortcuts import redirect

"""
Esta funcion verifica si un usuario tiene 3 o mas reservaciones en las cuales no se presento.
Si se detecta que tiene 3 o mas reservaciones sin presentarse se suspende al usuario por 30 dias
"""
def verificateSuspention(request):
	if request.user.is_anonymous():
		return HttpResponseRedirect('/login')
	else:
		fecha_actual = date.today()
		usuario = UserProfile.objects.get(user=request.user)
		reservaciones = Reservation.objects.filter(user=usuario,verificated=False,date__lte=fecha_actual)
		if reservaciones.count()>3:
			usuario.suspended=True
			usuario.dateSuspended=fecha_actual
			usuario.save()
			for reservacion in reservaciones:
				reservacion.verificated=True
				reservacion.save()
			#retorno True porque quedo suspendido el usuario
			return True
		else:
			#retorno False porque no quedo suspendido el usuario
			return False

"""
Esta vista redirecciona a la vista correspondiente,dependiendo de si el usuario logueado es un usuario 
comun o si el usuario es un usuario propietario.
En caso de que el usuario logueado sea un usuario con permisos de usuario comun,verifica si esta
habilitado para realizar reservas
"""
def reservationCreate(request):
	try:
		usuario = UserProfile.objects.get(user=request.user)
	except Exception:
		return HttpResponseRedirect('/login')
	if usuario.userType=='CM':
		if usuario.suspended==True:
			dias = date.today()-usuario.dateSuspended
			countDays = abs(dias.days)
			if countDays>=30:
				usuario.suspended=False
				usuario.save()
				return HttpResponseRedirect('/addreservationCommonUser')
			else:
				message = """Oops!!! ha ocurrido un inconveniente,estas suspendido debido a que has
							acumulado 3 inasistencias.El periodo de suspensión es de 30 días,
							te quedan """+str(object=30-countDays)+""" dias de suspensión.Para más 
							información contactanos"""
				sendmail=True
				return render_to_response('404.html',{'message':message,'sendmail':sendmail})
		else:
			status = verificateSuspention(request)
			if not status:
				return HttpResponseRedirect('/addreservationCommonUser')
			else:
				message = """Oops!!! ha ocurrido un inconveniente,estas suspendido debido a que has
							acumulado 3 inasistencias.El periodo de suspensión es de 30 días.Para más 
							información contactanos"""
				sendmail=True
				return render_to_response('404.html',{'message':message,'sendmail':sendmail})				
			
	else:
		return HttpResponseRedirect('/addreservationOwnerUser')
	

class CreateReservationAsCommonUser(CreateView):
	model = Reservation
	success_url = '/reservations'
	form_class = ReservationFormCommonUser
	
	#restricted area for anonymous users
	#@method_decorator(login_required)
    	def dispatch(self, *args, **kwargs):
    		if self.request.user.is_anonymous():
    			return HttpResponseRedirect('/login')
    		try:
    			usuario = UserProfile.objects.get(user=self.request.user)
    		except Exception:
    			return HttpResponseRedirect('/login')
    		if usuario.userType=='CM':
				return super(CreateReservationAsCommonUser, self).dispatch(*args, **kwargs)
    		else:
				message = """Oops!!! ha ocurrido un inconveniente, no tienes permiso para 
							realizar reservaciones a canchas.Para más información contactanos"""
				sendmail=True
				return render_to_response('404.html',{'message':message,'sendmail':sendmail})

	def get_context_data(self, **kwargs):
	    # Call the base implementation first to get a context
	    context = super(CreateReservationAsCommonUser, self).get_context_data(**kwargs)
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
    		

	#set the user that's logged in as the user that make the reservation
	def form_valid(self, form):
			try:
				user_logued = UserProfile.objects.get(user=self.request.user)
			except Exception:
				return HttpResponseRedirect('/login')
			form.instance.user = user_logued
			reservas = Reservation.objects.filter(date=form.instance.date,hour=form.instance.hour,minutes=form.instance.minutes,court=form.instance.court).count()
			fecha_actual = date.today()
			if reservas == 0 and form.instance.date>=fecha_actual:
				return super(CreateReservationAsCommonUser, self).form_valid(form)
			else:
				if reservas == 0:
					message = """Oops!!! ha ocurrido un inconveniente, ya existe una reservación para la 
								 misma cancha en el mismo día y horario.Intente en otro dia o horario u cancha"""
				else:
					message = """Oops!!! ha ocurrido un inconveniente, la fecha de la reservación debe ser desde """+str(object=fecha_actual)+" en adelante"									
				reservation=True
				return render_to_response('404.html',{'message':message,'reservation':reservation},RequestContext(self.request, {}))


class CreateReservationAsOwnerUser(CreateView):
	model = Reservation
	success_url = '/reservations'
	form_class = ReservationFormOwnerUser
	
	#restricted area for anonymous users
  	def dispatch(self, *args, **kwargs):
    		if self.request.user.is_anonymous():
    			return HttpResponseRedirect('/login')
    		try:
    			usuario = UserProfile.objects.get(user=self.request.user)
    		except Exception:
    			return HttpResponseRedirect('/login')
    		if usuario.userType=='PR':
				return super(CreateReservationAsOwnerUser, self).dispatch(*args, **kwargs)
    		else:
				message = """Oops!!! ha ocurrido un inconveniente, no tienes permiso para 
							realizar reservaciones a canchas.Para más información contactanos"""
				sendmail=True
				return render_to_response('404.html',{'message':message,'sendmail':sendmail})

	def get_context_data(self, **kwargs):
	    # Call the base implementation first to get a context
	    context = super(CreateReservationAsOwnerUser, self).get_context_data(**kwargs)
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

	#set the user that's logged in as the user that make the reservation
	def form_valid(self, form):
			reservas = Reservation.objects.filter(date=form.instance.date,hour=form.instance.hour,minutes=form.instance.minutes,court=form.instance.court).count()
			fecha_actual = date.today()
			if reservas == 0 and form.instance.date>=fecha_actual:
				#form.instance.user_logued = self.request.user
				return super(CreateReservationAsOwnerUser, self).form_valid(form)
			else:
				if reservas == 0:
					message = """Oops!!! ha ocurrido un inconveniente, ya existe una reservación para la 
								 misma cancha en el mismo día y horario.Intente en otro dia o horario u cancha"""
				else:
					message = """Oops!!! ha ocurrido un inconveniente, la fecha de la reservación debe ser desde """+str(object=fecha_actual)+" en adelante"									
				reservation=True
				return render_to_response('404.html',{'message':message,'reservation':reservation},RequestContext(self.request, {}))

	def get_form_kwargs(self):
    		kwargs = super(CreateReservationAsOwnerUser, self).get_form_kwargs()
    		kwargs.update({'user_logued': self.request.user})
    		return kwargs				
	
"""
Esta vista se encarga de listar reservaciones.Para ello el usuario debe estar logueado.
Si el usuario tiene permisos de usuario comun solo mostrará aquellas reservaciones que lo tiene 
asociado como responsable.
Si el usuario tiene permisos de usuario propietario solo mostrará las reservaciones asociadas a complejos
en donde es propietario
"""
class listReservations(ListView):
	template_name = 'reservations/listReservations.html'
	model = Reservation
	context_object_name = 'reservations' # Nombre de la lista a recorrer desde listReservations.html
	paginate_by = 6

  	def dispatch(self, *args, **kwargs):
    		if self.request.user.is_anonymous():
    			return HttpResponseRedirect('/login')
    		else:
    			return super(listReservations, self).dispatch(*args, **kwargs)
    		

	def get_queryset(self):
		try:
			usuario = UserProfile.objects.get(user=self.request.user)
		except Exception:
			return HttpResponseRedirect('/login')
		if usuario.userType=='CM':
			return Reservation.objects.filter(user_id=UserProfile.objects.get(user=self.request.user))
		else:
			return Reservation.objects.filter(court=Court.objects.filter(complex=Complex.objects.filter(user=self.request.user)))

	def get_context_data(self, **kwargs):
	    # Call the base implementation first to get a context
	    context = super(listReservations, self).get_context_data(**kwargs)
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
Esta vista se encarga de cancelar una reservacion.Para ello el usuario debe estar logueado y debe
tener permisos de usuario propietario
"""
class markAsAttended(UpdateView):
	model = Reservation
	fields = ['attended']
	template_name_suffix = '_update_form' # This is: modelName_update_form.html
	success_url = '/reservations'

   	def dispatch(self, *args, **kwargs):
   		if self.request.user.is_anonymous():
   			return HttpResponseRedirect('/login')
   		else:
	   		try:
	   			usuario = UserProfile.objects.get(user=self.request.user)
	   		except Exception:
	   			return HttpResponseRedirect('/login')
	   		if usuario.userType=='PR':
	   		    return super(markAsAttended, self).dispatch(*args, **kwargs)
	   		else:
	   			message = """
	   					  Oops!!! ha ocurrido un inconveniente, no tienes los permisos necesarios para 
	   					  indicar la asistencia a esta reservacion.Para mayor información contactese.
	   					  """
	   			sendmail = True
	   			return render_to_response('404.html',{'message':message,'sendmail':sendmail})
   	    
   	
   	def get_object(self,queryset=None):
   		reserva = super(markAsAttended, self).get_object()
   		try:
   			usuario = UserProfile.objects.get(user=self.request.user)
   		except Exception:
   			raise Http404
   		fecha_actual = date.today()
   		if reserva.court.complex.user == self.request.user:
   			return reserva
   		else:
   			raise Http404

	def get_context_data(self, **kwargs):
	    # Call the base implementation first to get a context
	    context = super(markAsAttended, self).get_context_data(**kwargs)
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
Esta vista se encarga de cancelar una reservacion.Para ello el usuario debe estar logueado
"""


def cancelReservation(request,id_reservation):
	if request.user.is_anonymous():
		return HttpResponseRedirect('/login')
	else:
		try:
			fecha_actual = date.today()
			reserva = Reservation.objects.get(id=id_reservation)
			usuario = UserProfile.objects.get(user = request.user)
		except Exception:
				message = '''
						   Oops!!! ha surgido un inconveniente.
						  '''
				listreservation = True
				return render_to_response('404.html',{'message':message,'listreservation':listreservation}, RequestContext(request, {}))
		if request.POST:
			if usuario.userType=='CM':
				if reserva.user == usuario and fecha_actual< reserva.date:
					reserva.delete()
					return HttpResponseRedirect('/reservations')
				else:
					message = '''
							   Oops!!! ha surgido un inconveniente, no es posible cancelar esta reservación.Recuerde que para 
							   cancelar una reservación deberá contar con 24 horas de anterioridad como mínimo.
							  '''
					listreservation = True
					return render_to_response('404.html',{'message':message,'listreservation':listreservation}, RequestContext(request, {}))				
			else:
				if fecha_actual<=reserva.date and reserva.court.complex.user == request.user:
					reserva.delete()
					return HttpResponseRedirect('/reservations')
				else:
					message = '''
							   Oops!!! ha surgido un inconveniente, no es posible cancelar esta reservación.Recuerde que para 
							   cancelar una reservación tiene tiempo hasta el dia de la reserva,pasado ese tiempo no puede 
							   cancelar dicha reservación.
							  '''
					listreservation = True
					return render_to_response('404.html',{'message':message,'listreservation':listreservation}, RequestContext(request, {}))					
		else:
			if reserva != None:
				return render_to_response('reservations/reservation_confirm_delete.html',{'reserva':reserva}, RequestContext(request, {}))