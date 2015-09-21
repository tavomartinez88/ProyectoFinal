#encoding:utf-8
from django.test import TestCase
from proyectoFinal.citys.models import City
from proyectoFinal.telephones.models import Telephone
from proyectoFinal.courts.models import Court
from proyectoFinal.complexes.models import Complex
from proyectoFinal.users.models import UserProfile
from django.contrib.auth.models import User

class CourtTestCase(TestCase):
    def setUp(self):
    	ciudad = City.objects.create(name='Venado Tuerto', postCode=2600)
    	tel = Telephone.objects.create(number = '154864587')
    	user_one=User.objects.create_user(username='tavo',email='gmartinezgranella@gmail.com',password='tavo',last_name='martinez',first_name='gustavo')
    	userprofile_one = UserProfile.objects.create(firstname=user_one.first_name,
    												 lastname=user_one.last_name,
    												 email = user_one.email,
    												 username = user_one.username,
    												 password = 'tavo',
    												 telephone = tel,
    												 city= ciudad,
    												 user = user_one,
    												 userType = 'PR',)

    	user_two=User.objects.create_user(username='cris',email='cris_09@hotmail.com',password='cris',last_name='martinez',first_name='cristian')
    	tel2 = Telephone.objects.create(number = '427144')
    	userprofile_two = UserProfile.objects.create(firstname=user_two.first_name,
    												 lastname=user_two.last_name,
    												 email = user_two.email,
    												 username = user_two.username,
    												 password = 'cris',
    												 telephone = tel2,
    												 city= ciudad,
    												 user = user_two,
    												 userType = 'CM',)    	

    	Complex.objects.create(name='Oxigeno',streetAddress='Cerrito 1159', roaster=True,buffet=True,lockerRoom=True,user=userprofile_one.user)


    """
    Este test verifica la correcta creacion de una cancha asociada a un complejo
    """
    def test_courts_create(self):
    	usuario = UserProfile.objects.get(username='tavo', password='tavo')
    	#verifico que el usuario tiene permisos de propietario
    	self.assertEqual(usuario.userType, 'PR')
    	complejo = Complex.objects.get(name = 'Oxigeno', streetAddress = 'Cerrito 1159')
    	#verifico que el usuario que registro el complejo y el logueado(en este caso es 'usuario') son el mismo
    	self.assertEqual(usuario.user, complejo.user)
    	#verifico que no tengo canchas inicialmente con los datos sumisnistrados
    	self.assertEqual(Court.objects.filter(complex=complejo,name='1A').count(), 0)
    	Court.objects.create(artificial_light=True, lawnType='Futsal', soccerType='Futbol 5', complex=complejo, name='1A')
    	#luego de la creación ahora deberia haber un cambio en la bd conteniendo un registro en la bd en la tabla 
    	#courts_court en base a los datos sumisnitrados
    	self.assertEqual(Court.objects.filter(complex=complejo,name='1A').count(), 1)

    """
    Este test verifica la correcta actualización de una determinada cancha
    """
    def test_courts_update(self):
    	#creo en forma auxiliar una cancha para actualizar
    	complejo = Complex.objects.get(name = 'Oxigeno', streetAddress = 'Cerrito 1159')
    	cancha = Court.objects.create(artificial_light=True, lawnType='Futsal', soccerType='Futbol 5', complex=complejo, name='1A')
    	usuario = UserProfile.objects.get(username='tavo', password='tavo')
    	#verifico que el usuario que va actualizar la cancha tiene permisos de propietario
    	self.assertEqual(usuario.userType, 'PR')
    	#verifico que el usuario que va a actualizar la cancha es el mismo que el dueño del complejo donde esta 
    	#registrada la cancha.
    	self.assertEqual(cancha.complex.user, usuario.user)
    	cancha.artificial_light=False
    	cancha.name='La bombonera'
    	cancha.save()
    	self.assertEqual(Court.objects.filter(name='La bombonera',artificial_light=False).count(), 1)

    """
    Este test verifica la correcta eliminación de una determinada cancha
    """
    def test_courts_delete(self):
    	#creo en forma auxiliar una cancha para delete
    	complejo = Complex.objects.get(name = 'Oxigeno', streetAddress = 'Cerrito 1159')
    	cancha = Court.objects.create(artificial_light=True, lawnType='Futsal', soccerType='Futbol 5', complex=complejo, name='1A')
    	usuario = UserProfile.objects.get(username='tavo', password='tavo')
    	#verifico que el usuario que va a realizar la eliminacion de la cancha tiene permisos de propietario
    	self.assertEqual(usuario.userType, 'PR')
    	#verifico que el usuario que va a eliminar la cancha es el mismo que el dueño del complejo donde esta 
    	#registrada la cancha.
    	self.assertEqual(cancha.complex.user, usuario.user)
    	#verifico que tengo un cancha para eliminar
    	self.assertNotEqual(Court.objects.filter(name='1A').count(), 0)
    	cancha.delete()
    	#verifico que ya no cuento con la cancha luego de la eliminacion
    	self.assertEqual(Court.objects.filter(name='1A').count(), 0)

    """
    Este test verifica el listado de canchas en forma correcta
    """
    def test_courts_list(self):
    	#creo en forma auxiliar unas canchas para listar
    	complejo = Complex.objects.get(name = 'Oxigeno', streetAddress = 'Cerrito 1159')
    	cancha1 = Court.objects.create(artificial_light=True, lawnType='Futsal', soccerType='Futbol 5', complex=complejo, name='1A')
    	cancha2 = Court.objects.create(artificial_light=True, lawnType='Futsal', soccerType='Futbol 5', complex=complejo, name='2A')
    	cancha3 = Court.objects.create(artificial_light=True, lawnType='Futsal', soccerType='Futbol 5', complex=complejo, name='3A')
    	#obtengo en forma auxiliar dos usuarios para identificar los casos para un usuario CM y un usuario PR
    	usuario1 = UserProfile.objects.get(username='tavo', password='tavo')
    	usuario2 = UserProfile.objects.get(username='cris', password='cris')
    	#verifico si el usuario es CM
    	self.assertEqual(usuario2.userType, 'CM')
    	#genero las canchas que voy a retornar
    	Court.objects.filter(complex=complejo)
    	#verifico si el usuario es PR
    	self.assertEqual(usuario1.userType, 'PR')
    	#si es PR ,verifico si el usuario es el mismo que el que registro el complejo donde estan alojadas las canchas
    	#esto es muy util para que un usuario PR no pueda ver canchas ajenas
    	self.assertEqual(usuario1.user, complejo.user)
    	#muestro las canchas correspondientes
    	Court.objects.filter(complex=complejo)

    """
    Este test verifica la busqueda de canchas en forma correcta
    """
    def test_courts_search(self):
    	#creo en forma auxiliar unas canchas para listar
    	complejo = Complex.objects.get(name = 'Oxigeno', streetAddress = 'Cerrito 1159')
    	cancha1 = Court.objects.create(artificial_light=True, lawnType='Futsal', soccerType='Futbol 5', complex=complejo, name='1A')
    	cancha2 = Court.objects.create(artificial_light=True, lawnType='Futsal', soccerType='Futbol 5', complex=complejo, name='2A')
    	cancha3 = Court.objects.create(artificial_light=True, lawnType='Futsal', soccerType='Futbol 5', complex=complejo, name='3A')
    	courts = Court.objects.filter(complex__name__icontains='Oxigeno').distinct()
        self.assertTrue(courts.count()>0)
