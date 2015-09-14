from django import forms
from models import PlayersInfo
from proyectoFinal.complexes.models import Complex
from proyectoFinal.tournaments.models import Tournament
from proyectoFinal.teams.models import Team
from proyectoFinal.users.models import UserProfile

class PlayerForm(forms.ModelForm):
    class Meta:
        model = PlayersInfo
        fields = ('goals', 'yellowCards', 'redCards')
        widgets = {
        	'goals': forms.TextInput(attrs={'class':'form-control','type':'number'}),
        	'yellowCards': forms.TextInput(attrs={'class':'form-control','type':'number'}),
        	'redCards': forms.TextInput(attrs={'class':'form-control','type':'number'}),
        	
    	}

    def __init__(self, *args, **kwargs):
        super(PlayerForm, self).__init__(*args, **kwargs)        