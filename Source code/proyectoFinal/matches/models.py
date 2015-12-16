from django.db import models

from proyectoFinal.teams.models import Team
from proyectoFinal.fixtures.models import Fixture
from proyectoFinal.courts.models import Court

class Match(models.Model):
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
	day = models.DateField(verbose_name='Selecccionar fecha')
	#score = models.CharField(max_length=6,blank=True, null=True,verbose_name='Resultado')
	scoreLocal = models.IntegerField(default=0,null=True,blank=True)
	scoreVisit = models.IntegerField(default=0,null=True,blank=True)
	hour = models.IntegerField(choices= hour_choices, verbose_name='Seleccionar hora')
	minutes = models.IntegerField(choices= minutes_choices,verbose_name='Seleccionar minutos')
	teamlocal = models.ForeignKey(Team, related_name='Seleccionar equipo local' ,blank=True, null=True, on_delete=models.CASCADE,verbose_name='Nombre del equipo local')
	teamVisitant = models.ForeignKey(Team, related_name='Seleccionar equipo visitante' ,blank=True, null=True, on_delete=models.CASCADE,verbose_name='Nombre del equipo visitante')
	fixture = models.ForeignKey(Fixture, blank=True, null=True, on_delete=models.CASCADE, verbose_name='Seleccionar fixture del torneo al que pertenece el partido')
	court = models.ForeignKey(Court, on_delete=models.CASCADE, verbose_name = 'Seleccionar cancha')

	def __str__(self):
		return '%s  %s' %(self.teamlocal.name,self.teamVisitant.name)
