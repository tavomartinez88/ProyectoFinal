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