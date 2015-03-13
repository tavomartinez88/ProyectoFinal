from django.db import models
from proyectoFinal.users.models import User
#from proyectoFinal.tournaments.models import Tournament

class Team(models.Model):
	name = models.CharField(max_length=50, verbose_name='Nombre del equipo')
	captain = models.ForeignKey(User, related_name='captain', verbose_name='Capitan/Delegado')
	players = models.ManyToManyField(User, related_name='player', verbose_name='Jugadores')

	def __str__(self):
		return '%s' %(self.name)