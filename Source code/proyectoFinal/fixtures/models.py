from django.db import models

class Fixture(models.Model):
	
	date = models.DateField(verbose_name='Fecha')
	
	def __str__(self):
		return '%s %s' %(self.id , self.date)
