#encoding:utf-8
from django.db import models
from proyectoFinal.users.models import User

# Create your models here.

class Publicity(models.Model):
	title = models.CharField(max_length= 30, verbose_name='Nombre de publicidad')
	img = models.FileField(upload_to='publicities',verbose_name='Seleccionar imagen')
	user = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='Id del usuario')

	def __str__(self):
		return '%s' %(self.title)

	class Admin:
		pass		
