from django import forms
from models import Match


class MatchForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = ('day', 'hour', 'minutes', 'teamlocal' , 'teamVisitant')
        widgets = {
            #'name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nombre del equipo'}),
            #'day':forms.DateInput(format="%m/%d/%Y")
 			'day':forms.DateInput(attrs={'class':'form-control', 'type':'date'},format="%Y/%m/%d"),
 			'hour':forms.Select(attrs={'class':'form-control'}),
 			'minutes':forms.Select(attrs={'class':'form-control'}),
 			'teamlocal':forms.Select(attrs={'class':'form-control'}),
 			'teamVisitant':forms.Select(attrs={'class':'form-control'}),

        }        

    def __init__(self, *args, **kwargs):
        super(MatchForm, self).__init__(*args, **kwargs)

class MatchFormUpdate(forms.ModelForm):
    class Meta:
        model = Match
        fields = ('scoreLocal', 'scoreVisit')
       

    def __init__(self, *args, **kwargs):
        super(MatchFormUpdate, self).__init__(*args, **kwargs)
        self.fields['scoreLocal'].widget.attrs.update({'class': 'form-control'})
        self.fields['scoreVisit'].widget.attrs.update({'class': 'form-control'})               