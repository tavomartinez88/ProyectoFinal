#encoding:utf-8
from django.test import TestCase
from proyectoFinal.citys.models import City
from proyectoFinal.telephones.models import Telephone
from proyectoFinal.users.models import UserProfile
from django.contrib.auth.models import User

"""
The next class provide testing implementation for User,UserProfile and Telephone
"""


class UserTestCase(TestCase):
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
    """
    El siguiente test verifica las condiciones necesarias para poder registrar un usuario correctamente.
    Verifica unicamente que entre dos usuarios tengan los campos email y user  distintos.Con respecto al username
    tambien deben ser distintos pero no se verifica utilizando un assert pues al momento de querer registrar dos
    usuarios con el mismo username ,el modelo lanza una excepcion por el echo de utilizar el tag unique
    """    
    def test_users_register(self):
    	tel = Telephone.objects.create(number = '154864587')
    	city = City.objects.get(name='Venado Tuerto', postCode=2600)

    	#obtiene un usuario ya creado y crea uno nuevo
    	user_one = User.objects.get(username='tavo',email='gmartinezgranella@gmail.com')
    	user_two=User.objects.create_user(username='ariel',email='arielmartinezgranella.com',password='tavo',last_name='martinez',first_name='gustavo')

    	#obtiene un perfil ya creado y crea uno nuevo
    	perfil_1 = UserProfile.objects.get(email='gmartinezgranella@gmail.com',username='tavo')
    	perfil_2 = UserProfile.objects.create(firstname=user_two.first_name,
    										  lastname=user_two.last_name,
    										  email = user_two.email,
    										  username = user_two.username,
    										  telephone = tel,
    										  city= city,
    										  user = user_two,
    										  userType = 'PR')
    	if perfil_2.userType == 'PR':
    		user_two.is_active = False
    		user_two.save()

    	#verifica que el usuario user_one esta activo
    	self.assertEqual(user_one.is_active,True)	
    	#verifica que el usuario user_one no esta activo
    	self.assertEqual(user_two.is_active,False)
    	#verifica que no existe otro usuario con el mismo email
    	self.assertNotEqual(user_one.email,user_two.email)
    	#verifica que no existen 2 perfil con un mismo usuario
    	self.assertNotEqual(perfil_1.user.id,perfil_2.user.id)

	"""
	user_current representa un usuario logueado,entonces verifico si user_for_delete y user_current tienen el mismo id.
	Entonces eso implicaría que perfil que se está intentando eliminar el usuario logueado es dueño 
	"""

    def test_users_delete(self):
    	user_current = User.objects.get(username='tavo')
    	user_for_delete = UserProfile.objects.get(email='gmartinezgranella@gmail.com')
    	self.assertEqual(user_current.id, user_for_delete.user.id)
    	user_for_delete.delete()
    	self.assertEqual(UserProfile.objects.filter(email='gmartinezgranella@gmail.com').count(), 0)


	"""
	Defino un usuario que representa al usuario logueado (user_current) y busco un usuario para actualizar el perfil
	por lo tanto el test verifica que el perfil del usuario a modificar corresponde al usuario logueado
	-la nueva direccion de email no deberia ser ocupada por ningun otro usuario
	-un usuario no deberia poder cambiar de categoria(tipo de usuario)
	"""

    def test_users_userUpdate(self):
    	user_current = User.objects.get(username = 'tavo')
    	user_for_update = UserProfile.objects.get(email = 'gmartinezgranella@gmail.com')
    	self.assertEqual(user_current.id, user_for_update.user.id)
    	self.assertEqual(user_current.email, user_for_update.email)

    	#actualización del email del usuario
    	user_for_update.email = 'gmartinez@gmail.com'
    	self.assertEqual(UserProfile.objects.filter(email=user_for_update.email).count(), 0)
    	user_for_update.save()


    	#Un usuario no deberia poder cambiarse de categoria pues de ser asi podria quedar complejos y las relaciones que 
    	#conlleva colgadas
    	typeUser_old = user_for_update.userType
    	typeUser_new = 'PR'
    	self.assertEqual(typeUser_old, typeUser_new)
    	user_for_update.userType=typeUser_new
    	user_for_update.save()

	"""
	Defino un usuario que representa al usuario logueado (user_current) y busco un usuario para actualizar el telefono
	por lo tanto el test verifica que el telefono del usuario a modificar corresponde al usuario logueado
	-un usuario no deberia poder cambiar el telefono de otro usuario
	"""
    def test_users_telephoneUpdate(self):
    	user_current = User.objects.get(username = 'tavo')
    	user_for_update = UserProfile.objects.get(email = 'gmartinezgranella@gmail.com')
    	self.assertEqual(user_current.id, user_for_update.user.id)
    	user_for_update.telephone.number='427144'
    	user_for_update.save()    	