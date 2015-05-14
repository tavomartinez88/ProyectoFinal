from django.db import models
from proyectoFinal.complexes.models import Complex

class Court(models.Model):
	CESPED_NATURAL = 'CN'
	CESPED_SINTETICO = 'CS'
	FUTSAL = 'FS'
	FUTBOL5 = 'F5'
	FUTBOL7 = 'F7'
	FUTBOL11 = 'F11'
	artificial_light = models.BooleanField()
	lawnType_choices = (
		(CESPED_NATURAL, 'Cesped Natural'),
		(CESPED_SINTETICO, 'Cesped Sintetico'),
		(FUTSAL, 'Futsal')
		)
	soccerType_choices = (
		(FUTBOL5, 'Futbol 5'),
		(FUTBOL7, 'Futbol 7'),
		(FUTBOL11, 'Futbol 11')
		)
	lawnType = models.CharField(max_length=23, choices=lawnType_choices, default=CESPED_SINTETICO,verbose_name='Tipo de cesped')
	soccerType = models.CharField(max_length=23, choices=soccerType_choices, default=FUTBOL5, verbose_name='Tipo de cancha')
	complex = models.ForeignKey(Complex, on_delete=models.CASCADE, verbose_name='Complejo propietario')
	def __str__(self):
		return '%s %s %s' %(self.get_lawnType_display(), self.get_soccerType_display(), self.complex.name)

# Create your models here.
