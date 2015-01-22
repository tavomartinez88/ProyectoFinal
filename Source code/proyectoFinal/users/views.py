from django.db.models import Q
from django.shortcuts import render_to_response
from models import User
from forms import UserForm
from django.http import HttpResponseRedirect
from django.views.generic import ListView, UpdateView
from django.core.context_processors import csrf # to increase security in the page

class listUser(ListView):
	template_name = 'users/listUsers.html'
	model = User

class userUpdate(UpdateView):
	model = User
	fields = ['email', 'telephones', 'city']
	template_name_suffix = '_update_form'

def register(request):
	if request.POST:
		form = UserForm(request.POST) #create a UserForm
		if form.is_valid(): #if the information in the form its correct
			form.save()
			return HttpResponseRedirect('/users')
	else:
		form = UserForm()
	args = {}
	args.update(csrf(request))
	args['form'] = form
	return render_to_response('users/register.html', args)