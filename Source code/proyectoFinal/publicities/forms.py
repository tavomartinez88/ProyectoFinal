from django import forms
from models import Publicity

class PublicityForm(forms.ModelForm):

    class Meta:
        model = Publicity
        fields = ['title', 'img']
        widgets = {
        	'title': forms.TextInput(attrs={'class':'form-control'}),        	
    	}        

    def __init__(self, *args, **kwargs):
        super(PublicityForm, self).__init__(*args, **kwargs)

class PublicityFormUpdate(forms.ModelForm):

    class Meta:
        model = Publicity
        fields = ['title', 'img']
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control'}),           
        }        

    def __init__(self, *args, **kwargs):
        super(PublicityFormUpdate, self).__init__(*args, **kwargs)