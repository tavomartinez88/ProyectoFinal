from django import forms
from models import UserProfile, Telephone

class UserForm(forms.ModelForm):
	class Meta: 
		model = UserProfile
		widgets = {
        	'password': forms.PasswordInput(), # Hide the entered information 
    	}
		fields = ('firstname' , 'lastname', 'email', 'username', 'password', 'city', 'userType')

class TelephoneForm(forms.ModelForm):
	class Meta:
		model = Telephone
		fields = ('number',)		