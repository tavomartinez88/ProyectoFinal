from django.db import models

# Create your models here.
class Telephone(models.Model):
	number = models.CharField(max_length=9)

	def createTelephone(self, numero):
		num = Telephone(number = numero)
		num.save()	



class LandLine(models.Model):
	areaCode = models.CharField(max_length=6)
	Id_number = models.ForeignKey(Telephone)

	def createLandLine(self, codeArea, numero):
		cod = LandLine(areaCode = codeArea)
		cod.save()
		num = Telephone(number = numero)
		num.save()


	def __str__(self):
		numero = Telephone.objects.filter(id = Id_number)
		return '%s%s%s'%(self.areaCode,'-',numero.number)

	class Meta:
                ordering = ["Id_number"]


class CellPhone(models.Model):
	Id_number = models.ForeignKey(Telephone)

	def createCellPhone(self,numero):
		num = Telephone(number = numero)
		num.save()

	def __str__(self):
		numero = Telephone.objects.filter(id = Id_number)
		return '%s'%(numero.number)

	class Meta:
                ordering = ["Id_number"]


					