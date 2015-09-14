#encoding:utf-8
from django import forms

class FormularioContacto(forms.Form):
	Nombre = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control','placeholder':'Ingrese su nombre'}))
	Email = forms.EmailField(widget=forms.TextInput(attrs={'class' : 'form-control','placeholder':'Ingrese su correo electrónico'}))
	Asunto = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control','placeholder':'Ingrese el asunto'}))
	Mensaje = forms.CharField(widget=forms.Textarea(attrs={'class' : 'form-control','placeholder':'Ingrese su mensaje'}))