from django.db import models

class Complejo(models.Model):
  nombre=models.CharField(max_length=20)
  direccion=models.CharField(max_length=20)
  telefono=models.CharField(max_length=15)
  nombreTitular=models.CharField(max_length=20)

  def __str__(self):
  	 return ' %s %s %s %s '%(self.nombre,self.direccion,self.telefono,self.nombreTitular)
  class Meta:
  	ordering = ["nombre"]

  class Admin:
  	pass	
