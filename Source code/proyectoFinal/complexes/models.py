from django.db import models

from proyectoFinal.users.models import User

class Complex(models.Model):
	name = models.CharField(max_length=25)
	streetAddress = models.CharField(max_length=25)
	roaster = models.BooleanField()
	buffet = models.BooleanField()
	lockerRoom = models.BooleanField()
	user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
  
	def __str__(self):
		return '%s %s'%(self.name, self.streetAddress)