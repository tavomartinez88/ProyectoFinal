from django.db import models
from django.contrib.auth.models import User
from proyectoFinal.telephones.models import Telephone
from proyectoFinal.citys.models import City


class User(models.Model):
	#user = models.ForeignKey(User, unique=True)
	firstname = models.CharField(max_length=40)
	lastname =  models.CharField(max_length=40)
	email = models.EmailField()
	username = models.CharField(max_length=60)
	password = models.CharField(max_length=60)
	telephones = models.ManyToManyField(Telephone, blank=True)
	city = models.ForeignKey(City)

	def __str__(self):
		return ' %s %s' % (self.firstname, self.lastname)

