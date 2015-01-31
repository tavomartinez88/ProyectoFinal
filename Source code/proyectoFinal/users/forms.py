from django import forms
from models import User

class UserForm(forms.ModelForm):
	class Meta: 
		model = User
		widgets = {
        	'password': forms.PasswordInput(), # Hide the entered information 
    	}
		fields = ('firstname' , 'lastname', 'email', 'username', 'password', 'telephone', 'city')

