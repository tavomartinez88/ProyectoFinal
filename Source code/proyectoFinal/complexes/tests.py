#encoding:utf-8
from django.test import TestCase
from proyectoFinal.citys.models import City
from proyectoFinal.telephones.models import Telephone
from proyectoFinal.users.models import UserProfile
from django.contrib.auth.models import User
from proyectoFinal.complexes.models import Complex

class ComplexTestCase(TestCase):
	#Este metodo realiza todas las inicializaciones basicas necesarias.
    def setUp(self):
    	ciudad = City.objects.create(name='Venado Tuerto', postCode=2600)
    	tel_pr = Telephone.objects.create(number = '154864587')
    	user_one=User.objects.create_user(username='tavo',email='gmartinezgranella@gmail.com',password='tavo',last_name='martinez',first_name='gustavo')
    	userprofile_one = UserProfile.objects.create(firstname=user_one.first_name,
    												 lastname=user_one.last_name,
    												 email = user_one.email,
    												 username = user_one.username,
    												 password = 'tavo',
    												 telephone = tel_pr,
    												 city= ciudad,
    												 user = user_one,
    												 userType = 'PR',)

    	tel_cm = Telephone.objects.create(number = '435507')
    	user_cm=User.objects.create_user(username='miguel',email='miguelgranella@gmail.com',password='granella',last_name='granella',first_name='miguel')
    	userprofile_one = UserProfile.objects.create(firstname=user_cm.first_name,
    												 lastname=user_cm.last_name,
    												 email = user_cm.email,
    												 username = user_cm.username,
    												 password = 'granella',
    												 telephone = tel_cm,
    												 city= ciudad,
    												 user = user_cm,
    												 userType = 'CM',)    	
  	
  	"""
  	El siguiente test verifica la creación de un complejo
  	-el usario logueado debe ser propietario
  	-pertenecer al staff de minutogol
  	"""
    def test_complexes_register(self):
    	owner_user = UserProfile.objects.get(username='tavo', password='tavo')
    	owner_user.user.is_staff = True
    	owner_user.user.save()
    	self.assertEqual(owner_user.userType, 'PR')
    	self.assertEqual(owner_user.user.is_staff, True)
    	Complex.objects.create(name='Oxigeno',
    						   streetAddress='Cerrito 1159',
    						   roaster=True,buffet=True,lockerRoom=True,user=owner_user.user)
    	self.assertNotEqual(Complex.objects.filter(name='Oxigeno').count(), 0)


    """
    El siguiente test verifica la actualización de un complejo 
    -el usuario logueado debe ser propietario
    -el usuario logueado y el usuario asociado al complejo deben ser el mismo
    """

    def test_complexes_update(self):
    	#owner_user representa al usuario logueado el cual debe ser propieatrio
    	owner_user = UserProfile.objects.get(username='tavo', password='tavo')
    	self.assertEqual(owner_user.userType, 'PR')
    	#creo un objeto complex,el cual se va a actualizar más adelante
    	Complex.objects.create(name='Oxigeno',
    						   streetAddress='Cerrito 1159',
    						   roaster=True,buffet=True,lockerRoom=True,user=owner_user.user)    	
    	#obtengo el complex a actualizar
    	complejo = Complex.objects.get(name='Oxigeno')
    	#verifico que el propietario del complejo es el usuario logueado(en este caso owner_user)
    	self.assertEqual(owner_user.user.id, complejo.user.id)
    	complejo.name='Doble 5'
    	complejo.save()
    	#Como tenia 1 solo objeto cuyo nombre del complejo era 'Oxigeno',luego de la actualizacion
    	#deberia no tener ningun objeto cuyo nombre sea oxigeno

    	self.assertEqual(Complex.objects.filter(name='Oxigeno').count(), 0)

    """
    El siguiente test verifica la eliminación de un complejo 
    -el usuario logueado debe ser propietario
    -el usuario logueado y el usuario asociado al complejo deben ser el mismo
    """

    def test_complexes_delete(self):
    	#owner_user representa al usuario logueado el cual debe ser propieatrio
    	owner_user = UserProfile.objects.get(username='tavo', password='tavo')
    	self.assertEqual(owner_user.userType, 'PR')
    	#creo un objeto complex,el cual se va a eliminar más adelante
    	Complex.objects.create(name='Oxigeno',
    						   streetAddress='Cerrito 1159',
    						   roaster=True,buffet=True,lockerRoom=True,user=owner_user.user)    	
    	#obtengo el complex a eliminar
    	complejo = Complex.objects.get(name='Oxigeno')
    	#verifico que el propietario del complejo es el usuario logueado(en este caso owner_user)
    	self.assertEqual(owner_user.user.id, complejo.user.id)
    	complejos_antes = Complex.objects.all().count()
    	complejo.delete()
    	complejos_despues = Complex.objects.all().count()
    	#Luego de la eliminacion deberia tener uno menos 
    	self.assertEqual(complejos_antes, complejos_despues+1)

    """
    El siguiente test verifica la busqueda de complejos 
    """

    def test_search_complex(self):
    	#las 3 primeras lineas son auxiliares a lo que respecta al test en si,pues son
    	#necesarias para poder desarrollar la busqueda de complejos

    	#obtengo un usuario propietario que va a ser el propietario del complejo
    	owner_user = UserProfile.objects.get(username='tavo', password='tavo')
    	#verifico que el usuario posee la categoria de propietario(y no de user comun)
    	self.assertEqual(owner_user.userType, 'PR')
    	Complex.objects.create(name='Oxigeno',
    						   streetAddress='Cerrito 1159',
    						   roaster=True,buffet=True,lockerRoom=True,user=owner_user.user)    	

    	#la siguiente linea emula la operacion like de sql
    	countComplex=Complex.objects.filter(name__contains="Oxi").distinct().count()
    	#verifica que se ha encontrado un objeto de acuerdo al patron de busqueda
    	self.assertTrue(countComplex > 0)


    """
    El siguiente test verifica el listado de complejos 
    """    	
    def test_list_complexes(self):
    	#las 3 primeras lineas son auxiliares a lo que respecta al test en si,pues son
    	#necesarias para poder desarrollar la busqueda de complejos

    	#obtengo un usuario propietario que va a ser el propietario del complejo
    	owner_user = UserProfile.objects.get(username='tavo', password='tavo')
    	#verifico que el usuario posee la categoria de propietario(y no de user comun)
    	self.assertEqual(owner_user.userType, 'PR')
    	Complex.objects.create(name='Oxigeno',
    						   streetAddress='Cerrito 1159',
    						   roaster=True,buffet=True,lockerRoom=True,user=owner_user.user)
    	Complex.objects.create(name='Doble 5',
    						   streetAddress='asd 1234',
    						   roaster=True,buffet=True,lockerRoom=True,user=owner_user.user)
    	usuario = UserProfile.objects.get(username='miguel', password='granella')
    	#si el usuario es invitado o es un usuario comun retorno todos los complejos disponibles
    	self.assertEqual(usuario.userType, 'CM')
    	Complex.objects.all()
    	#si el usuario es un usuario propietario retorno todos los complejos en 
    	#donde el usuario propietario en cuestion es el dueño de dichos complejos
    	self.assertEqual(owner_user.userType, 'PR')
    	Complex.objects.filter(user = usuario.user)    	   	