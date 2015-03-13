from django.db import models
from proyectoFinal.users.models import User
from proyectoFinal.courts.models import Court

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
	user = models.ForeignKey(User, verbose_name='Usuario')
	court = models.ForeignKey(Court, verbose_name='Cancha')