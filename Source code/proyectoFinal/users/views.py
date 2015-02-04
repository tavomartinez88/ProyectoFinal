from django.db.models import Q
from django.shortcuts import render_to_response
from models import User, Telephone
from forms import UserForm, TelephoneForm
from django.http import HttpResponseRedirect
from django.views.generic import ListView, UpdateView, DetailView
from django.core.context_processors import csrf # to increase security in the page
from django.template import RequestContext

class listUser(ListView):
	template_name = 'users/listUsers.html'
	model = User
	context_object_name = 'users' # Nombre de la lista a recorrer desde listUsers.html

class userUpdate(UpdateView):
	model = User
	fields = ['email', 'city', 'password', 'userType']
	template_name_suffix = '_update_form'
	success_url = '/users' #redirect when the edit form is filled

	#INVESTIGATE THIS.. 
	#def get_context_data(self, **kwargs):
	#	context = super(userUpdate, self).get_context_data(**kwargs)
	#	context['telephone'] = Telephone.objects.get(number=358422829)
	#	return context

	#AND THIS..
	#extra_context = {"Telefono" : Telephone.objects.filter(number=358422829)}


class telephoneUpdate(UpdateView):
	model = Telephone
	fields = ['number',]
	template_name_suffix = '_update_form'
	success_url = '/update_user/1' #redirect when the edit form is filled

def register(request):
	if request.POST:
		form = UserForm(request.POST) #create a UserForm
		tform = TelephoneForm(request.POST)
		if form.is_valid() and tform.is_valid(): #if the information in the form its correct
			user = form.save(commit=False) #first prepare the user model, but dont commit it yet to the database
			user.telephone = tform.save() #add the telephone id to the user model, and save the telephone model
			user.save() #save the user model
			return HttpResponseRedirect('/users')
	else:
		form = UserForm()
		tform = TelephoneForm()
	return render_to_response('users/register.html', {'form': form, 'tform': tform}, RequestContext(request, {}))