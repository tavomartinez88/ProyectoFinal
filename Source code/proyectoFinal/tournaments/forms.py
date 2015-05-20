from django import forms
from models import Tournament
from proyectoFinal.complexes.models import Complex

class TournamentForm(forms.ModelForm):
    class Meta:
        model = Tournament
        fields = ['name', 'teams', 'complex']

    def __init__(self, user, *args, **kwargs):
        super(TournamentForm, self).__init__(*args, **kwargs)
        self.fields['complex'] = forms.ModelChoiceField(queryset=Complex.objects.filter(user=user))