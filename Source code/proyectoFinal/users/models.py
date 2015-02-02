from django.db import models
from proyectoFinal.telephones.models import Telephone
from proyectoFinal.citys.models import City

class User(models.Model):
	COMUN = 'CM'
	PROPIETARIO = 'PR'
	firstname = models.CharField(max_length=40)
	lastname =  models.CharField(max_length=40)
	email = models.EmailField(unique=True)
	username = models.CharField(max_length=60, unique=True)
	password = models.CharField(max_length=60)
	telephone = models.OneToOneField(Telephone, unique=False)
	city = models.ForeignKey(City)
	userType_choices = (
		(COMUN, 'Usuario comun'),
		(PROPIETARIO, 'Propietario de complejo')
		)
	userType = models.CharField(max_length=23, choices=userType_choices, default=COMUN)

	def __str__(self):
		return ' %s %s' % (self.first_name, self.last_name)

