from django.db import models
from proyectoFinal.telephones.models import Telephone

class User(models.Model):
	firstname = models.CharField(max_length=40)
	lastname =  models.CharField(max_length=40)
	email = models.EmailField()
	username = models.CharField(max_length=60)
	password = models.CharField(max_length=60)
	telephones = models.ManyToManyField(Telephone)

	def __str__(self):
		return ' %s %s' % (self.first_name, self.last_name)

