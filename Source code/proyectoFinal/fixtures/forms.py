from django import forms
from models import Fixture
from models import Tournament
from proyectoFinal.complexes.models import Complex

class FixtureForm(forms.ModelForm):
    class Meta:
        model = Fixture
        

    def __init__(self, user, *args, **kwargs):
        super(FixtureForm, self).__init__(*args, **kwargs)
        self.fields['tournament'] = forms.ModelChoiceField(queryset=Tournament.objects.filter(complex=Complex.objects.filter(user=user)))
        