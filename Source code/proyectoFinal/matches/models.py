from django.db import models

from proyectoFinal.teams.models import Team

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
	day = models.DateField(verbose_name='Fecha')
	score = models.CharField(max_length=6,blank=True, null=True,verbose_name='Resultado')
	hour = models.IntegerField(choices= hour_choices, verbose_name='Hora')
	minutes = models.IntegerField(choices= minutes_choices,verbose_name='Minutos')
	teamlocal = models.ForeignKey(Team, related_name='Equipo local' ,blank=True, null=True, on_delete=models.CASCADE,verbose_name='Nombre del equipo local')
	teamVisitant = models.ForeignKey(Team, related_name='Equipo visitante' ,blank=True, null=True, on_delete=models.CASCADE,verbose_name='Nombre del equipo visitante')
	
	def __str__(self):
		return '%s  %s' %(self.teamlocal.name,self.teamVisitant.name)



