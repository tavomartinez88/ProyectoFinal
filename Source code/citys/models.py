from django.db import models

# Create your models here.
class City(models.Model):
	name = models.CharField(max_length=30)
	postCode = models.IntegerField()
	

	def __str__(self):
			return '%s%i'% (self.name, self.postCode)

	class Meta:
		ordering = ["name"]		


