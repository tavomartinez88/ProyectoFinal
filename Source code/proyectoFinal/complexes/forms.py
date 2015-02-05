from django import forms
from models import Complex


class ComplexForm(forms.ModelForm):
	class Meta:
		model = Complex
		fields = ('name','streetAddress','roaster','buffet','lockerRoom')		