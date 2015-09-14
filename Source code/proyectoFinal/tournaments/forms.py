#encoding:utf-8
from django import forms
from models import Tournament
from proyectoFinal.complexes.models import Complex

class TournamentForm(forms.ModelForm):
    class Meta:
        model = Tournament
        fields = ['name', 'teams', 'complex']

    def __init__(self, user, *args, **kwargs):
        super(TournamentForm, self).__init__(*args, **kwargs)
        self.fields['complex'] = forms.ModelChoiceField(queryset=Complex.objects.filter(user_id=user))
        for field in self.fields:
            # Recorremos todos los campos del modelo para añadirle class="form-control
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class TournamentFormUpdate(forms.ModelForm):
    class Meta:
        model = Tournament
        fields = ['inProgress', 'teams']

    def __init__(self, *args, **kwargs):
        super(TournamentFormUpdate, self).__init__(*args, **kwargs)       
        self.fields['teams'].widget.attrs.update({'class': 'form-control'})           