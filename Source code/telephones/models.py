from django.db import models

# Create your models here.
class Telephone(models.Model):
	number = models.CharField(max_length=9)

	def __str__(self):
		return '%s'%(self.number)

	 

#class LandLine(models.Model):
#	areaCode = models.CharField(max_length=6)
#	Id_number = models.ForeignKey(Telephone)




#class CellPhone(models,Model):
#	Id_number = models.ForeignKey(Telephone)



					