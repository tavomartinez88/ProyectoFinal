from django import forms
from models import User

class UserForm(forms.ModelForm):
	class Meta: 
		model = User
		fields = ('firstname' , 'lastname', 'email', 'username', 'password', 'city')

