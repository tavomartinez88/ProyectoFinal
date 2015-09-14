#encoding:utf-8
from django import forms
from models import Fixture
from models import Tournament
from proyectoFinal.complexes.models import Complex

class FixtureForm(forms.ModelForm):
    class Meta:
        model = Fixture
        widgets = {
            'date':forms.DateInput(attrs={'class':'form-control', 'type':'date'},format="%Y/%m/%d"),
        }            
        

    def __init__(self, user, *args, **kwargs):
        super(FixtureForm, self).__init__(*args, **kwargs)
        self.fields['tournament'] = forms.ModelChoiceField(queryset=Tournament.objects.filter(complex=Complex.objects.filter(user=user)))
        for field in self.fields:
            # Recorremos todos los campos del modelo para añadirle class="form-control
            self.fields['name'].widget.attrs.update({'class': 'form-control','placeholder':'Ingrese el nombre del fixture'})
            
            self.fields['tournament'].widget.attrs.update({'class': 'form-control'})

class FixtureFormUpdate(forms.ModelForm):
    class Meta:
        model = Fixture
        fields = ['name','date']
        widgets = {
            'date':forms.DateInput(attrs={'class':'form-control', 'type':'date'},format="%Y/%m/%d"),
        }
        

    def __init__(self, user, *args, **kwargs):
        super(FixtureFormUpdate, self).__init__(*args, **kwargs)
        for field in self.fields:
            # Recorremos todos los campos del modelo para añadirle class="form-control
            self.fields['name'].widget.attrs.update({'class': 'form-control','placeholder':'Ingrese el nombre del fixture'})
            
