#encoding:utf-8
from django import forms
from models import Complex


class ComplexForm(forms.ModelForm):
	class Meta:
		model = Complex
		fields = ('name','streetAddress','roaster','buffet','lockerRoom')
		widgets = {
        	'name': forms.TextInput(attrs={'class':'form-control','placeholder':'Nombre'}),
        	'streetAddress': forms.TextInput(attrs={'class':'form-control','placeholder':'Dirección'}),
        	'roaster': forms.CheckboxInput(attrs={'class':'checkbox'}),
        	'buffet': forms.CheckboxInput(attrs={'class':'checkbox'}),
        	'lockerRoom': forms.CheckboxInput(attrs={'class':'checkbox'}),
    	}		