from django import forms
from models import Reservation
from proyectoFinal.users.models import UserProfile


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['date', 'hour', 'minutes', 'user', 'court']

    def __init__(self, *args, **kwargs):
        super(ReservationForm, self).__init__(*args, **kwargs)
        self.fields['user'] = forms.ModelChoiceField(queryset=UserProfile.objects.filter(userType="CM"))