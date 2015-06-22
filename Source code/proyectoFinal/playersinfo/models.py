from django.db import models
from proyectoFinal.users.models import UserProfile
from proyectoFinal.tournaments.models import Tournament

class PlayersInfo(models.Model):

	goals = models.PositiveIntegerField(verbose_name='Goles', blank='True')
	yellowCards = models.PositiveIntegerField(verbose_name='Tarjetas Amarillas', blank='True')
	redCards = models.PositiveIntegerField(verbose_name='Tarjetas Rojas', blank='True')
	user = models.ForeignKey(UserProfile, verbose_name='Usuario')
	tournament = models.ForeignKey(Tournament, verbose_name='Torneo')