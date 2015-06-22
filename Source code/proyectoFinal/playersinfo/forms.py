from django import forms
from models import PlayersInfo
from proyectoFinal.complexes.models import Complex
from proyectoFinal.tournaments.models import Tournament
from proyectoFinal.teams.models import Team
from proyectoFinal.users.models import UserProfile

"""class PlayerInfoForm(forms.ModelForm):
    class Meta:
        model = PlayersInfo
        fields = ['goals', 'yellowCards', 'redCards', 'tournament']

    def __init__(self, user, *args, **kwargs):
        super(PlayerInfoForm, self).__init__(*args, **kwargs)
        self.fields['user'] = forms.ModelChoiceField(queryset=UserProfile.objects.filter(queryset=Teams.objects.filter(queryset=Tournament.objects.filter(queryset=Complex.objects.filter(user=user))    
"""

class PlayerForm(forms.ModelForm):
    class Meta:
        model = PlayersInfo
        fields = ('goals', 'yellowCards', 'redCards', 'tournament')