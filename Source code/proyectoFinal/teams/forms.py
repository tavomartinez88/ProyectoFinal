#encoding:utf-8
from django import forms
from models import Team
from proyectoFinal.users.models import UserProfile
from django.contrib.auth.models import User

class TeamFormUpdate(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'captain', 'players']
        widgets = {
        	'name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nombre del equipo'}),
        	'players': forms.Select(attrs={'class':'form-control'}),
        	'captain': forms.Select(attrs={'class':'form-control'}),

    	}


    def __init__(self, *args, **kwargs):
        super(TeamFormUpdate, self).__init__(*args, **kwargs)
        self.fields['players'] = forms.ModelMultipleChoiceField(queryset=UserProfile.objects.filter(userType='CM'))
        self.fields['captain'] = forms.ModelChoiceField(queryset=User.objects.filter(is_staff=0))
        for field in self.fields:
            # Recorremos todos los campos del modelo para añadirle class="form-control
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'players']
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nombre del equipo'}),
 

        }


    def __init__(self, *args, **kwargs):
        super(TeamForm, self).__init__(*args, **kwargs)
        #self.fields['players'] = forms.ModelMultipleChoiceField(queryset=User.objects.filter(is_staff=0))
        self.fields['players'] = forms.ModelMultipleChoiceField(queryset=UserProfile.objects.filter(userType='CM'))
        self.fields['players'].widget.attrs.update({'class': 'form-control'})


