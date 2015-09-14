#encoding:utf-8
from django.db import models
from django.contrib.auth.models import User
from proyectoFinal.telephones.models import Telephone
from proyectoFinal.citys.models import City

class UserProfile(models.Model):
	COMUN = 'CM'
	PROPIETARIO = 'PR'
	firstname = models.CharField(max_length=40, verbose_name='Nombre')
	lastname =  models.CharField(max_length=40, verbose_name='Apellido')
	email = models.EmailField(unique=True)
	username = models.CharField(max_length=60, unique=True, verbose_name='Nombre de usuario')
	password = models.CharField(max_length=60, verbose_name='Contraseña')
	telephone = models.OneToOneField(Telephone, unique=False, verbose_name='Telefono')
	city = models.ForeignKey(City, verbose_name='Ciudad')
	user = models.ForeignKey(User) # Extends the default User model provided by Django
	userType_choices = (
		(COMUN, 'Usuario comun'),
		(PROPIETARIO, 'Propietario de complejo')
		)
	userType = models.CharField(max_length=23, choices=userType_choices, default=COMUN, verbose_name='Tipo de usuario')
	suspended = models.BooleanField(default=False,blank=True)
	dateSuspended = models.DateField(default='2015-01-01')

	class Meta:
		ordering = ['lastname', 'firstname']

	def __unicode__(self):
		return ' %s' % (self.email)


