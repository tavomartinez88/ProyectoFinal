#Las funcionalidades propuesta abajo auqnue se dejan por si son de utilidad no seran necesarias puesto 
#que el framework django provee metodos que realizan el mismo trabajo
from django.db import models

# Create your models here.
class Telephone(models.Model):
	number = models.CharField(max_length=9)


class LandLine(models.Model):
	areaCode = models.CharField(max_length=6)
	Id_number = models.ForeignKey(Telephone)

	def createLandLine(self, numero, area):
		num = Telephone(number = numero)
		num.save()
		fijo = LandLine(Id_number = num.id, areaCode = area)
		fijo.save()
		

	def deleteLandLine(self, numero, area):
		num = Telephone.objects.get(number = numero, areaCode = area)
		num.delete()

	def updateLandLine(self, numberNow, numberNew,areaNow, areaNew):
		num = Telephone.objects.get(number = numberNow)
		cod = LandLine.objects.get(Id_number = num.id, areaCode = areaNow)
		
		if ((numberNew != "") and (areaNew!= "") and (num != null) and (cod != null)) :
			cod.areaCode = areaNew
			num.number = numberNew
			num.save()
			cod.save()
		
		if numberNew == "" and areaNew!= "" and num != null and cod != null :
			cod.areaCode = areaNew
			cod.save()			

		if numberNew != "" and areaNew == "" and num != null and cod != null :
			num.number = numberNew
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
		cell = CellPhone(Id_number = num.id)
		num.save()
		cell.save()

	def deleteCellPhone(self, numero):
		num = Telephone.objects.get(number = numero)
		if num != null:
			num.delete()
		else :
			print "el numero no existe"	

	def updateCellPhone(self, numberNow, numberNew):
		num = Telephone.objects.get(number = numberNow)
		if num != null :
			num.number=numberNew
			num.save()
		else :
			print "el numero no existe"			


	def __str__(self):
		numero = Telephone.objects.filter(id = Id_number)
		return '%s'%(numero.number)

	class Meta:
                ordering = ["Id_number"]				