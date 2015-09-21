#encoding:utf-8
from django import forms
from models import Reservation
from models import Court
from proyectoFinal.complexes.models import Complex
from proyectoFinal.users.models import UserProfile
from django.contrib.admin import widgets 
from django.forms.widgets import DateInput , DateTimeInput, TimeInput
from django.contrib.admin.widgets import AdminDateWidget
from datetime import date




class ReservationFormCommonUser(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['date', 'hour', 'minutes', 'court']
        widgets = {
        	'court': forms.Select(attrs={'class':'form-control'}),
        	'hour': forms.Select(attrs={'class':'form-control'}),
        	'minutes': forms.Select(attrs={'class':'form-control'}),
        	#'date':forms.DateInput(attrs={'class':'form-control', 'type':'date'},format="%Y/%m/%d"),
            'date':forms.DateInput(attrs={'class':'form-control', 'id':'datepicker'},format="%d/%m/%Y"),
    	}

    def __init__(self, *args, **kwargs):
        super(ReservationFormCommonUser, self).__init__(*args, **kwargs)

class ReservationFormOwnerUser(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['date', 'hour', 'minutes', 'user','court']
        widgets = {
            'court': forms.Select(attrs={'class':'form-control'}),
            'hour': forms.Select(attrs={'class':'form-control'}),
            'minutes': forms.Select(attrs={'class':'form-control'}),
            'user': forms.Select(attrs={'class':'form-control'}),
            'date':forms.DateInput(attrs={'class':'form-control', 'id':'datepicker'},format="%d/%m/%Y"),
        }

    def verificateSuspention(self,usuario):
        fecha_actual = date.today()
        reservaciones = Reservation.objects.filter(user=usuario,verificated=False,date__lte=fecha_actual)
        if reservaciones.count()>2:
            usuario.suspended=True
            usuario.dateSuspended=fecha_actual
            usuario.save()
            for reservacion in reservaciones:
                reservacion.verificated=True
                reservacion.save()
            #retorno True porque quedo suspendido el usuario
            return True
        else:
            #retorno False porque no quedo suspendido el usuario
            return False

    def __init__(self, user_logued, *args, **kwargs):
        super(ReservationFormOwnerUser, self).__init__(*args, **kwargs)
        usuarios = UserProfile.objects.filter(userType="CM")
        #print usuarios.count()
        for user_current in usuarios:
            if user_current.suspended==True:
                dias = date.today()-user_current.dateSuspended
                countDays = abs(dias.days)
                if countDays>=30:
                    user_current.suspended=False
                    user_current.save()
            else:
                self.verificateSuspention(user_current)
             

        self.fields['user'] = forms.ModelChoiceField(queryset=UserProfile.objects.filter(userType="CM", suspended=False))
        self.fields['court'] = forms.ModelChoiceField(queryset=Court.objects.filter(complex=Complex.objects.filter(user=user_logued)))
        for field in self.fields:
            # Recorremos todos los campos del modelo para añadirle class="form-control
            self.fields[field].widget.attrs.update({'class': 'form-control'})