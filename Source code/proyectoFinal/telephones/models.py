from django.db import models

# Create your models here.
class Telephone(models.Model):
	number = models.CharField(max_length=9, verbose_name='Telefono')

	def __str__(self):
		return '%s'%(self.number)

	class Meta:
         ordering = ["id"]				