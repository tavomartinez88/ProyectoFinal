from django.db.models import Q
from django.shortcuts import render_to_response
from models import UserProfile, Telephone
from forms import UserForm, TelephoneForm
from django.http import HttpResponseRedirect
from django.views.generic import ListView, UpdateView, DeleteView
from django.core.context_processors import csrf # to increase security in the page
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import Http404


def register(request):
	if request.POST:
		form = UserForm(request.POST) #create a UserForm
		tform = TelephoneForm(request.POST)
		if form.is_valid() and tform.is_valid(): #if the information in the form its correct
			#First, save the default User model provided by Django
			user = User.objects.create_user(
                	username=form.cleaned_data['username'],
					email=form.cleaned_data['email'], 
					password=form.cleaned_data['password'],
					last_name=form.cleaned_data['lastname'],
					first_name=form.cleaned_data['firstname']
                	)
			userProfile = form.save(commit=False) #then prepare the user model, but dont commit it yet to the database
			userProfile.user_id = user.id
			userProfile.telephone = tform.save() #add the telephone id to the user model, and save the telephone model
			userProfile.save() #save the user model
			if userProfile.userType == 'PR':
				user.is_active = False
        		user.save()
		return HttpResponseRedirect('/users')
	else:
		form = UserForm()
		tform = TelephoneForm()
	return render_to_response('users/register.html', {'form': form, 'tform': tform}, RequestContext(request, {}))

class listUser(ListView):
	template_name = 'users/listUsers.html'
	model = UserProfile
	context_object_name = 'users' # Nombre de la lista a recorrer desde listUsers.html

class userUpdate(UpdateView):
	model = UserProfile
	fields = ['email', 'city', 'password', 'userType']
	template_name_suffix = '_update_form'
	success_url = '/users' #redirect when the edit form is filled

class telephoneUpdate(UpdateView):
	model = Telephone
	fields = ['number',]
	template_name_suffix = '_update_form'
	success_url = '/update_user/1' #redirect when the edit form is filled

class deleteUser(DeleteView):
	model = UserProfile
	success_url = '/users'
	def get_object(self, queryset=None):
	  #select the user object that we want to delete
  	  obj = super(deleteUser, self).get_object()
  	  #if the user that we want to delete it's not the same that the user that's logged in
  	  if not obj.user == self.request.user:
  	      raise Http404
  	  return obj

def searchUser(request):
  query = request.GET.get('q', '')
  if query:
	qset = (Q(firstname__icontains=query) | 
			Q(lastname__icontains=query) |
			Q(username__icontains=query) |
			Q(email__icontains=query))
	results = UserProfile.objects.filter(qset).distinct()
  else:
	results = []
  return render_to_response("users/searchUser.html",{"results": results,"query": query})