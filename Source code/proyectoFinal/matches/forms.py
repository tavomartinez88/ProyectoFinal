from django import forms
from models import Match

class MatchForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = ('day', 'hour', 'minutes', 'teamlocal' , 'teamVisitant')
        
