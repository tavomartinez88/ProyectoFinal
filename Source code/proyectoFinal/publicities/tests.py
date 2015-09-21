#encoding:utf-8
from django.test import TestCase
from proyectoFinal.citys.models import City
from proyectoFinal.telephones.models import Telephone
from proyectoFinal.publicities.models import Publicity
from proyectoFinal.users.models import UserProfile
from django.contrib.auth.models import User
import datetime
from django.db.models import Q

class PlublicitiesTestCase(TestCase):
    def setUp(self):
    	ciudad = City.objects.create(name='Venado Tuerto', postCode=2600)
    	user_two=User.objects.create_user(username='cris',email='cris_09@hotmail.com',password='cris',last_name='martinez',first_name='cristian')
    	tel = Telephone.objects.create(number = '427144')
    	perfil_usuario = UserProfile.objects.create(firstname=user_two.first_name,
    												 lastname=user_two.last_name,
    												 email = user_two.email,
    												 username = user_two.username,
    												 password = 'cris',
    												 telephone = tel,
    												 city= ciudad,
    												 user = user_two,
    												 userType = 'PR',)
    	Publicity.objects.create(title='img',img='publicities/publish.jpg',user=perfil_usuario.user)

	"""
	Este test verifica la correcta creación de una publicidad correspondiente a un usuario logueado
	"""
    def test_publicities_create(self):
    	usuario_logued = UserProfile.objects.get(username='cris', password='cris')
    	self.assertFalse(usuario_logued.userType=='CM')
    	self.assertTrue(usuario_logued.userType=='PR')
    	publicidad = Publicity.objects.create(title='img1',img='publicities/qaaaa.jpg',user=usuario_logued.user)
    	self.assertTrue(publicidad.title=='img1' and publicidad.img=='publicities/qaaaa.jpg' and publicidad.user==usuario_logued.user)
    	self.assertEqual(Publicity.objects.filter(title='img1',img='publicities/qaaaa.jpg').count(), 1)

	"""
	Este test verifica la correcta actualización de una publicidad correspondiente a un usuario logueado
	"""
    def test_publicities_update(self):
    	usuario_logued = UserProfile.objects.get(username='cris', password='cris')
    	self.assertTrue(usuario_logued.userType=='PR')
    	publicidad = Publicity.objects.get(title='img', img='publicities/publish.jpg')
    	self.assertTrue(publicidad.user==usuario_logued.user)
    	self.assertEqual(Publicity.objects.filter(title='img',img='publicities/publish.jpg').count(), 1)
    	publicidad.title = 'publicidad nueva'
    	publicidad.img = 'publicities/photo.png'
    	publicidad.save()
    	self.assertEqual(Publicity.objects.filter(title='img',img='publicities/publish.jpg').count(), 0)
    	self.assertEqual(Publicity.objects.filter(title='publicidad nueva',img='publicities/photo.png').count(), 1)

	"""
	Este test verifica la correcta eliminación de una publicidad correspondiente a un usuario logueado
	"""
    def test_publicities_delete(self):
    	usuario_logued = UserProfile.objects.get(username='cris', password='cris')
    	self.assertTrue(usuario_logued.userType=='PR')
    	self.assertFalse(usuario_logued.userType=='CM')
    	publicidad = Publicity.objects.get(title='img', img='publicities/publish.jpg')
    	self.assertTrue(publicidad.user==usuario_logued.user)
    	self.assertEqual(Publicity.objects.filter(title='img',img='publicities/publish.jpg').count(), 1)
    	publicidad.delete()
    	self.assertEqual(Publicity.objects.filter(title='img',img='publicities/publish.jpg').count(), 0)

	"""
	Este test verifica la correcta lista de publicidades correspondiente a un usuario logueado
	"""
    def test_publicities_list(self):
    	usuario_logued = UserProfile.objects.get(username='cris', password='cris')
    	self.assertTrue(usuario_logued.userType=='PR')
    	self.assertTrue(Publicity.objects.filter(user=usuario_logued.user).count()>0)
    	self.assertFalse(usuario_logued.userType=='CM')
    	self.assertTrue(Publicity.objects.none().count()==0)

