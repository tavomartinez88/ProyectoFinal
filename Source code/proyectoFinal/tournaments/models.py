from django.db import models
from proyectoFinal.teams.models import Team
from proyectoFinal.complexes.models import Complex
#from proyectoFinal.fixtures.models import Fixture


class Tournament(models.Model):
	name = models.CharField(max_length=60, verbose_name='Nombre')
	inProgress = models.BooleanField(verbose_name='En juego', default='True')
	teams = models.ManyToManyField(Team, verbose_name='Equipos participantes')
	complex = models.ForeignKey(Complex, verbose_name='Complejo organizador') 
	#fixture = models.ForeignKey(Fixture)
