from django import forms
from models import Team
from proyectoFinal.users.models import UserProfile

class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'players']
        #__widgets = {"players": widgets.Select(attrs={"cols" : 180, "rows" : 15})
}

    def __init__(self, *args, **kwargs):
        super(TeamForm, self).__init__(*args, **kwargs)
        self.fields['players'] = forms.ModelMultipleChoiceField(queryset=UserProfile.objects.all(),required=True,widget=FilteredSelectMultiple("Jugadores",is_stacked=True))

