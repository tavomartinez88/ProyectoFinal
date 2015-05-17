from django import forms
from models import Court
from proyectoFinal.complexes.models import Complex

class CourtForm(forms.ModelForm):
    class Meta:
        model = Court
        fields = ['artificial_light', 'lawnType', 'soccerType', 'complex']

    def __init__(self, user, *args, **kwargs):
        super(CourtForm, self).__init__(*args, **kwargs)
        self.fields['complex'] = forms.ModelChoiceField(queryset=Complex.objects.filter(user=user))        
 