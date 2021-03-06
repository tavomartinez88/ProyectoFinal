#encoding:utf-8
from django.db.models import Q
from django.shortcuts import render_to_response
from models import UserProfile, Telephone
from proyectoFinal.publicities.models import Publicity
from forms import UserForm, TelephoneForm, UserUpdateForm
from django.http import HttpResponseRedirect
from django.views.generic import ListView, UpdateView, DeleteView
from django.core.context_processors import csrf # to increase security in the page
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse
from django.core.mail import send_mail



"""
Esta vista se encarga de la alta de un usuario
"""
def register(request):
	if request.user.is_active:
		return HttpResponseRedirect('/login')
	else:
		try:
			publish_one = Publicity.objects.all().order_by('?').first()
		except Exception:
			publish_one = False
		try:
			publish_second = Publicity.objects.all().exclude(id=publish_one.id).order_by('?').first()
		except Exception:
			publish_second = False
		if request.POST:
			form = UserForm(request.POST)
			tform = TelephoneForm(request.POST)
			if form.is_valid() and tform.is_valid():
				user = User.objects.create_user(username=form.cleaned_data['username'],email=form.cleaned_data['email'],password=form.cleaned_data['password'],last_name=form.cleaned_data['lastname'],first_name=form.cleaned_data['firstname'])
				userProfile = form.save(commit=False)
				userProfile.user_id = user.id
				userProfile.telephone = tform.save()
				userProfile.save()
				if userProfile.userType=='PR':
					user.is_active = False
					try:
						user.save()
					except Exception:
						raise Http404
				return HttpResponseRedirect('/login')
			else:
				mail = request.POST.get('email')
				nombreUsuario = request.POST.get('username')
				nombre = request.POST.get('firstname')
				apellido = request.POST.get('lastname')
				password = request.POST.get('password')
				telefono = request.POST.get('number')
				mensaje = ''
				status_nombre = False
				status_apellido = False
				status_mail = False
				status_nombreUsuario = False
				status_password = False
				status_telefono = False
				if len(nombre)<3 or nombre.isalpha()== False:
					status_nombre = True
				if len(apellido)<3 or apellido.isalpha()==False :
					status_apellido = True
				if len(mail)<6 or not '@' in mail or not '.com' in mail:
					status_mail = True
				if len(nombreUsuario)<6 or nombreUsuario.isalphanumeric()==False:
					status_nombreUsuario = True
				if len(password)<6 or password.isalnum():
				 	status_password = True
				if len(telefono)<6:
					status_telefono = True
				if status_nombre:
					mensaje = "Error al intentar registrarse, corregir los siguientes errores:\n"+"-El nombre debe contener mas de 2 caracteres(caracteres válidos a-z)\n"
				if status_apellido:
					mensaje = mensaje+"-El apellido debe contener mas de 2 caracteres(caracteres válidos a-z)\n"
				if status_password:
					mensaje = mensaje +"-La contraseña debe contener mas de 5 digitos y debe contener letras y al menos un numero\n"
				if status_telefono:
					mensaje = mensaje+"-El telefono debe estar compuesto unicamente por numeros y debe contener al menos 10 digitos\n"
				return render_to_response('users/register.html', {'mensaje':mensaje}, RequestContext(request, {}))
		else:
			form = UserForm()
			tform = TelephoneForm()
		return render_to_response('users/register.html',{'form':form, 'tform':tform, 'publish_one':publish_one, 'publish_second':publish_second}, RequestContext(request,{}))

"""
Esta vista se encarga de actualizar el perfil,el usuario debe estar logueado
"""
class userUpdate(UpdateView):
	model = UserProfile
	form_class = UserUpdateForm
	template_name_suffix = '_update_form'
	success_url = '/' #redirect when the edit form is filled
	context_object_name = 'userToUpdate'

	def get_context_data(self, **kwargs):
	    # Call the base implementation first to get a context
	    context = super(userUpdate, self).get_context_data(**kwargs)
	    # Add in the publisher
	    try:
	    	context['publish_one'] = Publicity.objects.all().order_by('?').first()
	    except Exception:
	    	context['publish_one'] = False
	    try:
	    	context['publish_second'] = Publicity.objects.all().exclude(id=context['publish_one'].id).first()
	    except Exception:
	    	context['publish_second'] = False
	    try:
	    	context['publish_third'] = Publicity.objects.all().order_by('?').exclude(id=context['publish_one'].id).exclude(id=context['publish_second'].id).first()
	    except Exception:
	    	context['publish_third'] = False
	    return context


	def get_form_kwargs(self):
			kwargs = super(userUpdate, self).get_form_kwargs()
			return kwargs

	def dispatch(self, *args, **kwargs):
		if self.request.user.is_anonymous():
			return HttpResponseRedirect('/login')
		return super(userUpdate, self).dispatch(*args, **kwargs)

	def get_object(self,queryset=None):
	   	usuario = super(userUpdate, self).get_object()
	   	if not usuario.user == self.request.user:
	   		raise Http404
	   	return usuario

class telephoneUpdate(UpdateView):
	model = Telephone
	form_class = TelephoneForm
	template_name_suffix = '_update_form'
	success_url = None
	def get_success_url(self):
		#updateuser it's tag of route /update_user/id in url.py
		try:
			usuario=UserProfile.objects.get(user=self.request.user)
		except Exception:
			raise Http404
		return reverse("updateuser",args=str(usuario.id))

	def get_form_kwargs(self):
				kwargs = super(telephoneUpdate, self).get_form_kwargs()
				return kwargs

	def get_context_data(self, **kwargs):
	    # Call the base implementation first to get a context
	    context = super(telephoneUpdate, self).get_context_data(**kwargs)
	    # Add in the publisher
	    try:
	    	context['publish_one'] = Publicity.objects.all().order_by('?').first()
	    except Exception:
	    	context['publish_one'] = False
	    try:
	    	context['publish_second'] = Publicity.objects.all().exclude(id=context['publish_one'].id).first()
	    except Exception:
	    	context['publish_second'] = False
	    return context

	#@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		if self.request.user.is_anonymous():
			return HttpResponseRedirect('/login')
		return super(telephoneUpdate, self).dispatch(*args, **kwargs)


	def get_object(self,queryset=None):
	   	tel = super(telephoneUpdate, self).get_object()
	   	usuario = UserProfile.objects.get(user=self.request.user)
	   	if not usuario.user == self.request.user:
	   		raise Http404
	   	return tel

class deleteUser(DeleteView):
	model = UserProfile
	success_url = '/'
	def get_form_kwargs(self):
				kwargs = super(deleteUser, self).get_form_kwargs()
				return kwargs

	def dispatch(self, *args, **kwargs):
		if self.request.user.is_anonymous():
			return HttpResponseRedirect('/login')
		return super(deleteUser, self).dispatch(*args, **kwargs)

	def get_context_data(self, **kwargs):
	    # Call the base implementation first to get a context
	    context = super(deleteUser, self).get_context_data(**kwargs)
	    # Add in the publisher
	    try:
	    	context['publish_one'] = Publicity.objects.all().order_by('?').first()
	    except Exception:
	    	context['publish_one'] = False
	    try:
	    	context['publish_second'] = Publicity.objects.all().exclude(id=context['publish_one'].id).first()
	    except Exception:
	    	context['publish_second'] = False
	    return context

	def get_object(self, queryset=None):
	  #select the user object that we want to delete
  	  obj = super(deleteUser, self).get_object()
  	  #if the user that we want to delete it's not the same that the user that's logged in
  	  if not obj.user == self.request.user:
  	      raise Http404
  	  return obj
