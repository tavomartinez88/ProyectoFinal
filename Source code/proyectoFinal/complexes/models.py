from django.db import models

from proyectoFinal.users.models import User

class Complex(models.Model):
	name = models.CharField(max_length=25, verbose_name='Nombre')
	streetAddress = models.CharField(max_length=25,verbose_name='Direccion')
	roaster = models.BooleanField(verbose_name='Asador')
	buffet = models.BooleanField(verbose_name='Cantina')
	lockerRoom = models.BooleanField(verbose_name='Vestuarios')
	user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE,verbose_name='Id del usuario')
  
	def __str__(self):
		return '%s %s'%(self.name, self.streetAddress)