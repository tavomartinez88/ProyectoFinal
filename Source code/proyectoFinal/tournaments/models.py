from django.db import models
from proyectoFinal.teams.models import Team
from proyectoFinal.complexes.models import Complex

class Tournament(models.Model):
	name = models.CharField(max_length=60, verbose_name='Nombre')
	inProgress = models.BooleanField(verbose_name='En juego', default='True')
	teams = models.ManyToManyField(Team, related_name='team', verbose_name='Equipos participantes')
	complex = models.ForeignKey(Complex, related_name='complejo',verbose_name='Complejo organizador') 

	def __str__(self):
		return '%s' %(self.name)