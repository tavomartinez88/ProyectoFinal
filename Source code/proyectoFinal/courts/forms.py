#encoding:utf-8
from django import forms
from models import Court
from proyectoFinal.complexes.models import Complex

class CourtForm(forms.ModelForm):
    class Meta:
        model = Court
        fields = ['artificial_light', 'lawnType', 'soccerType', 'name','complex']
        widgets = {
        	'artificial_light': forms.CheckboxInput(),
        	'lawnType': forms.Select(attrs={'class':'form-control'}),
        	'soccerType': forms.Select(attrs={'class':'form-control'}),
            'name': forms.TextInput(attrs={'class':'form-control'}),
        	'complex': forms.Select(attrs={'class':'form-control'}),

    	}

    def __init__(self, user, *args, **kwargs):
        super(CourtForm, self).__init__(*args, **kwargs)
        self.fields['complex'] = forms.ModelChoiceField(queryset=Complex.objects.filter(user=user))
        self.fields['lawnType'].widget.attrs.update({'class': 'form-control'})    
        self.fields['soccerType'].widget.attrs.update({'class': 'form-control'})   
        self.fields['name'].widget.attrs.update({'class': 'form-control','placeholder':'Id o nombre de la cancha'})    
        self.fields['complex'].widget.attrs.update({'class': 'form-control'})

class CourtFormUpdate(forms.ModelForm):
    class Meta:
        model = Court
        fields = ['artificial_light', 'lawnType', 'soccerType', 'complex','name']
        widgets = {
            'artificial_light': forms.CheckboxInput(),
            'lawnType': forms.Select(attrs={'class':'form-control'}),
            'soccerType': forms.Select(attrs={'class':'form-control'}),
            'name': forms.TextInput(attrs={'class':'form-control'}),

        }

    def __init__(self, *args, **kwargs):
        super(CourtFormUpdate, self).__init__(*args, **kwargs)
        
        self.fields['lawnType'].widget.attrs.update({'class': 'form-control'})    
        self.fields['soccerType'].widget.attrs.update({'class': 'form-control'})  
        self.fields['name'].widget.attrs.update({'class': 'form-control','placeholder':'Id o nombre de la cancha'})      
        
