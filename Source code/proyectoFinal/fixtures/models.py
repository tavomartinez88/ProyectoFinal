from django.db import models
from proyectoFinal.tournaments.models import Tournament
class Fixture(models.Model):
	name = models.CharField(max_length=60, verbose_name='Nombre')
	date = models.DateField(verbose_name='Fecha de Inicio')
	tournament = models.ForeignKey(Tournament, null='False', blank='False')
	def __str__(self):
		return '%s %s' %(self.name , self.date)
