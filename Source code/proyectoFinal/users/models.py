from django.db import models
from proyectoFinal.telephones.models import Telephone
from proyectoFinal.citys.models import City

class User(models.Model):
	COMUN = 'CM'
	PROPIETARIO = 'PR'
	firstname = models.CharField(max_length=40, verbose_name='Nombre')
	lastname =  models.CharField(max_length=40, verbose_name='Apellido')
	email = models.EmailField(unique=True)
	username = models.CharField(max_length=60, unique=True, verbose_name='Nombre de usuario')
	password = models.CharField(max_length=60, verbose_name='Contrasena')
	telephone = models.OneToOneField(Telephone, unique=False, verbose_name='Telefono')
	city = models.ForeignKey(City, verbose_name='Ciudad')
	userType_choices = (
		(COMUN, 'Usuario comun'),
		(PROPIETARIO, 'Propietario de complejo')
		)
	userType = models.CharField(max_length=23, choices=userType_choices, default=COMUN, verbose_name='Tipo de usuario')

	def __str__(self):
		return ' %s %s' % (self.first_name, self.last_name)

