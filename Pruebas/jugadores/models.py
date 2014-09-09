from django.db import models

# Create your models here.

class jugadores(models.Model):
        nombre = models.CharField(max_length=30)
        apellido = models.CharField(max_length=30)
        dni = models.IntegerField()
        email = models.EmailField(max_length=40)
        tel1 = models.CharField(max_length=20)
        tel2 = models.CharField(max_length=20)
        direccion = models.CharField(max_length=60)
        username = models.CharField(max_length=20)
        password = models.CharField(max_length=20)

        def __str__(self):
                return '%s%s'% (self.nombre, self.apellido)

        class Meta:
                ordering = ["apellido"]



