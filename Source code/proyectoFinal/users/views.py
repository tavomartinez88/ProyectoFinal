from django.db.models import Q
from django.shortcuts import render_to_response
from models import User
from forms import UserForm, TelephoneForm
from django.http import HttpResponseRedirect
from django.views.generic import ListView, UpdateView
from django.core.context_processors import csrf # to increase security in the page

class listUser(ListView):
	template_name = 'users/listUsers.html'
	model = User
	context_object_name = 'users' # Nombre de la lista a recorrer desde listUsers.html

class userUpdate(UpdateView):
	model = User
	fields = ['email', 'telephone', 'city']
	template_name = 'user_update_form'

def register(request):
	if request.POST:
		form = UserForm(request.POST) #create a UserForm
		#tform = TelephoneForm(request.POST)
		if form.is_valid(): #if the information in the form its correct
			form.save()
			return HttpResponseRedirect('/users')
	else:
		form = UserForm()
		#tform = TelephoneForm()
	args = {}
	#args2 = {}
	args.update(csrf(request))
	args['form'] = form
	#args2['tform'] = tform
	return render_to_response('users/register.html', args)