#encoding:utf-8
from django.db.models import Q
from django.shortcuts import render_to_response
from models import Publicity
from forms import PublicityForm, PublicityFormUpdate
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.core.context_processors import csrf # to increase security in the page
from django.template import RequestContext
from django.contrib import admin
from proyectoFinal.users.models import UserProfile
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import Http404
from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy

"""
Esta vista se encarga de crear una nueva publicidad, el usuario que crea la publicidad
debe estar logueado y ademas debe tener permisos de usuario propietario
"""
def nueva_publicidad(request):
	if request.user.is_anonymous():
		return HttpResponseRedirect('/login')
	try:
		usuario = UserProfile.objects.get(user = request.user)
	except Exception:
		return HttpResponseRedirect('/login')
	if usuario.userType=='PR':
		try:
			publish_one = Publicity.objects.all().order_by('?').first()
		except Exception:
			publish_one = False
		try:
			publish_second = Publicity.objects.all().exclude(id=publish_one.id).order_by('?').last()
		except Exception:
			publish_second = False
		if request.method == 'POST':
			formulario = PublicityForm(request.POST, request.FILES)
			if formulario.is_valid():
				image = request.FILES['img']
				publicidad = Publicity(title=formulario.cleaned_data['title'],img=image,user=request.user)
				publicidad.save()
				message_ok = "success"
				formulario = PublicityForm()
				return render_to_response('publicities/nuevapublicidad.html',{'formulario':formulario,'message_ok':message_ok,'publish_one':publish_one,'publish_second':publish_second}, context_instance=RequestContext(request))	
			else:
				message_error = "error"
				return render_to_response('publicities/nuevapublicidad.html',{'formulario':formulario,'message_error':message_error,'publish_one':publish_one,'publish_second':publish_second}, context_instance=RequestContext(request))	

		else:
			formulario = PublicityForm()
		return render_to_response('publicities/nuevapublicidad.html',{'formulario':formulario,'publish_one':publish_one,'publish_second':publish_second}, context_instance=RequestContext(request))	
	else:
		message = """Oops!!! ha ocurrido un inconveniente, no tiene los permisos necesarios para cargar una 
					 nueva publicidad,intente más tarde si aún persiste el inconveniente contactese."""
		sendmail = True
		return render_to_response('404.html',{'message':message,'sendmail':sendmail})

"""
Esta vista se encarga de actualizar una publicidad, el usuario que actualiza la publicidad
debe estar logueado y ademas debe tener permisos de usuario propietario
"""
def update_publish(request,idpublicidad):
	if request.user.is_anonymous():
		return HttpResponseRedirect('/login')
	try:
		usuario = UserProfile.objects.get(user= request.user)
		publicacion = Publicity.objects.get(id=idpublicidad)		
	except Exception:
		message = """Oops!!! ha ocurrido un inconveniente, no se encontró la publicidad,intente más tarde si aún persiste el inconveniente contactese."""
		sendmail = True
		return render_to_response('404.html',{'message':message,'sendmail':sendmail})
	if usuario.userType=='PR' and publicacion.user == request.user:
		try:
			publish_one = Publicity.objects.all().order_by('?').first()
		except Exception:
			publish_one = False
		try:
			publish_second = Publicity.objects.all().exclude(id=publish_one.id).order_by('?').first()
		except Exception:
			publish_second = False
		if request.method == 'POST':			
			formulario = PublicityFormUpdate(request.POST, request.FILES)
			if formulario.is_valid():
				publicacion.title = formulario.cleaned_data['title']
				publicacion.img = request.FILES['img']
				publicacion.save()
				formulario = PublicityFormUpdate()
				return HttpResponseRedirect('/publicities')
			else:
				message_error = "error"
				return render_to_response('publicities/updatepublicidad.html',{'formulario':formulario,'message_error':message_error,'publish_one':publish_one,'publish_second':publish_second}, context_instance=RequestContext(request))	
		else:
			formulario = PublicityFormUpdate()
		return render_to_response('publicities/updatepublicidad.html',{'formulario':formulario,'publish_one':publish_one,'publish_second':publish_second}, context_instance=RequestContext(request))		
	else:
		message = """Oops!!! ha ocurrido un inconveniente, no tiene los permisos necesarios para actualizar
					 una publicidad,intente más tarde si aún persiste el inconveniente contactese."""
		sendmail = True
		return render_to_response('404.html',{'message':message,'sendmail':sendmail})

"""
Esta vista se encarga de la eliminación de una  publicidad, el usuario que elimina la publicidad
debe estar logueado y ademas debe tener permisos de usuario propietario
"""
class deletePublicity(DeleteView):
	model = Publicity
	success_url = '/publicities'
	def get_form_kwargs(self):
		kwargs = super(deletePublicity,self).get_form_kwargs()
		return kwargs

	
	def dispatch(self, *args, **kwargs):
		if self.request.user.is_anonymous():
			return HttpResponseRedirect('/login')
	  	try:
	  		usuario = UserProfile.objects.get(user= self.request.user)
	  	except Exception:
			message = """Oops!!! ha ocurrido un inconveniente, no tiene los permisos necesarios para cargar una 
						 nueva publicidad,intente más tarde si aún persiste el inconveniente contactese."""
			sendmail = True
			return render_to_response('404.html',{'message':message,'sendmail':sendmail})
		if usuario.userType=='PR':
			return super(deletePublicity,self).dispatch(*args, **kwargs)
		else:
			message = """Oops!!! ha ocurrido un inconveniente, no tiene los permisos necesarios 
						 para eliminar esta publicidad, intente más tarde si aún persiste el 
						 inconveniente contactese."""
			sendmail = True
			return render_to_response('404.html',{'message':message,'sendmail':sendmail})
		

	def get_object(self, queryset=None):
		publicidad = super(deletePublicity,self).get_object()
		
		if publicidad.user != self.request.user:
			message = """Oops!!! ha ocurrido un inconveniente, no tiene los permisos necesarios para eliminar 
						 esta publicidad,por no ser el dueño de la publicidad, contactesea por cualquier consulta."""
			sendmail = True
			return render_to_response('404.html',{'message':message,'sendmail':sendmail})
		return publicidad	

	def get_context_data(self, **kwargs):
	    # Call the base implementation first to get a context
	    context = super(deletePublicity, self).get_context_data(**kwargs)
	    # Add in the publisher
	    try:
	    	context['publish_one'] = Publicity.objects.all().order_by('?').first()
	    except Exception:
	    	context['publish_one'] = False
	  	try:
	  		context['publish_second'] = Publicity.objects.all().exclude(id=context['publish_one'].id).order_by('?').first()
	  	except Exception, e:
	  		context['publish_second'] = False
	    return context			


"""
Esta vista se encarga de listar las publicidades, el usuario que visualiza las publicidades
debe ser un usuario con permisos de usuario propietario
"""
class listPublish(ListView):
  template_name = 'publicities/listpublish.html'
  model = Publicity
  context_object_name = 'publicaciones'
  paginate_by = 3

  def get_queryset(self):
  	if self.request.user.is_anonymous():
  		return HttpResponseRedirect('/login')
  	try:
  		usuario = UserProfile.objects.get(user = self.request.user)
  		if usuario.userType == 'PR':
  			return Publicity.objects.filter(user=self.request.user)
  		else:
  			return Publicity.objects.none() 		
  	except Exception:
  		return HttpResponseRedirect('/login')

  def get_context_data(self, **kwargs):
  	context = super(listPublish, self).get_context_data(**kwargs)
	try:
	   	context['publish_one'] = Publicity.objects.all().order_by('?').first()
	except Exception:
	   	context['publish_one'] = False
	try:
	   	context['publish_second'] = Publicity.objects.all().exclude(id=context['publish_one'].id).first()
	except Exception:
	   	context['publish_second'] = False
	return context