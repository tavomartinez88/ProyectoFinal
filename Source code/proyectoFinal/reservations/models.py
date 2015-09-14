from django.db import models
from django.conf import settings
from proyectoFinal.users.models import UserProfile
from proyectoFinal.courts.models import Court
from django.contrib.auth.models import User

class Reservation(models.Model):
	minutes_choices = (
		(00,'00'),
		(30,'30'))
	hour_choices = (
		(14,'14'),
		(15,'15'),
		(16,'16'),
		(17,'17'),
		(18,'18'),
		(19,'19'),
		(20,'20'),
		(21,'21'),
		(22,'22'),
		(23,'23'),
		(00,'00'),)

	attended = models.BooleanField(verbose_name='Asistio', default=False)
	date = models.DateField(verbose_name='Fecha', help_text='DD/MM/AAAA')
	hour = models.IntegerField(choices= hour_choices, verbose_name='Hora')
	minutes = models.IntegerField(choices= minutes_choices,verbose_name='Minutos')
	user = models.ForeignKey(UserProfile, verbose_name='Usuario')
	court = models.ForeignKey(Court, verbose_name='Cancha')
	verificated = models.BooleanField(default=False)

	class Meta:
		ordering = ['-date']