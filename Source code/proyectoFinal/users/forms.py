#encoding:utf-8
from django import forms
from models import UserProfile, Telephone

class UserForm(forms.ModelForm):
	class Meta: 
		model = UserProfile
		widgets = {
        	'firstname': forms.TextInput(attrs={'class':'form-control','placeholder':'Nombre'}),
        	'lastname': forms.TextInput(attrs={'class':'form-control','placeholder':'Apellido'}),
        	'email': forms.EmailInput(attrs={'class':'form-control','placeholder':'E-mail'}),
        	'username': forms.TextInput(attrs={'class':'form-control','placeholder':'Nombre de usuario'}),
        	'password': forms.PasswordInput(attrs={'class':'form-control','placeholder':'Contraseña'}),
        	'city': forms.Select(attrs={'class':'form-control'}),
        	'userType': forms.Select(attrs={'class':'form-control'}), # Hide the entered information 
    	}
		fields = ('firstname' , 'lastname', 'email', 'username', 'password', 'city', 'userType')

class TelephoneForm(forms.ModelForm):
	class Meta:
		model = Telephone
		widgets = {
        	'number': forms.TextInput(attrs={'class':'form-control','placeholder':'Telefono'}),   
    	}
		fields = ('number',)	

class UserUpdateForm(forms.ModelForm):
    class Meta: 
        model = UserProfile
        widgets = {
            'email': forms.EmailInput(attrs={'class':'form-control','placeholder':'E-mail'}),
            'password': forms.PasswordInput(attrs={'class':'form-control','placeholder':'Contraseña'}),
            'city': forms.Select(attrs={'class':'form-control'}),
            
        }
        fields = ('email', 'password', 'city')  
    