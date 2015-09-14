#encoding:utf-8
from django.test import TestCase
from proyectoFinal.citys.models import City
from proyectoFinal.telephones.models import Telephone
from proyectoFinal.teams.models import Team
from proyectoFinal.courts.models import Court
from proyectoFinal.complexes.models import Complex
from proyectoFinal.users.models import UserProfile
from django.contrib.auth.models import User

class TeamTestCase(TestCase):
    def setUp(self):
    	ciudad = City.objects.create(name='Venado Tuerto', postCode=2600)
    	user_two=User.objects.create_user(username='cris',email='cris_09@hotmail.com',password='cris',last_name='martinez',first_name='cristian')
    	tel = Telephone.objects.create(number = '427144')
    	userprofile_two = UserProfile.objects.create(firstname=user_two.first_name,
    												 lastname=user_two.last_name,
    												 email = user_two.email,
    												 username = user_two.username,
    												 password = 'cris',
    												 telephone = tel,
    												 city= ciudad,
    												 user = user_two,
    												 userType = 'CM',)    	

    
    """
    Este test verifica la correcta creacion de un equipo
    """
    
    def test_teams_create(self):
    	usuario = UserProfile.objects.get(username='cris', password='cris')
    	#verifico que el usuario tiene permisos de usuario comun
    	self.assertEqual(usuario.userType, 'CM')
    	#creo por ej n usuarios en forma provisoria solo para poder crear un equipo esto en una view no hace falta
    	#pues los usuarios van a ir apareciendo de acuerdo a medida que vayan registrando los diferentes usuarios
    	user_1=User.objects.create_user(username='agustin',email='agustinO@hotmail.com',password='agustin',last_name='orion',first_name='agustin')
    	tel = Telephone.objects.create(number = '427140')
    	city = City.objects.get(name='Venado Tuerto', postCode=2600)
    	userprofile_1 = UserProfile.objects.create(firstname=user_1.first_name,
    												 lastname=user_1.last_name,
    												 email = user_1.email,
    												 username = user_1.username,
    												 password = 'agustin',
    												 telephone = tel,
    												 city= city,
    												 user = user_1,
    												 userType = 'CM',)
    	user_2=User.objects.create_user(username='cata',email='ddiaz@hotmail.com',password='daniel',last_name='diaz',first_name='daniel')
    	tel = Telephone.objects.create(number = '427141')
    	userprofile_2 = UserProfile.objects.create(firstname=user_2.first_name,
    												 lastname=user_2.last_name,
    												 email = user_2.email,
    												 username = user_2.username,
    												 password = 'daniel',
    												 telephone = tel,
    												 city= city,
    												 user = user_2,
    												 userType = 'CM',)
        #creo una instancia de Team indicando el nombre del equipo y su capitan
        #el capitan debe ser el mismo usuario que crea el equipo
    	equipo = Team.objects.create(name='Central Argentino',captain=usuario.user)
        #agrego los jugadores que formaran parte del equipo
        equipo.players.add(userprofile_1,userprofile_2,usuario)
        equipo.save()
        #Verifico que ahora cuento con un equipo cuyo nombre es 'Central Argentino'
        self.assertEqual(Team.objects.filter(name='Central Argentino').count(), 1)

    """
    Este test verifica el listado de equipos
    """

    def test_teams_list(self):
        usuario = UserProfile.objects.get(username='cris', password='cris')
        #verifico que el usuario tiene permisos de usuario comun
        self.assertEqual(usuario.userType, 'CM')
        #creo por ej n usuarios en forma provisoria solo para poder crear un equipo esto en una view no hace falta
        #pues los usuarios van a ir apareciendo de acuerdo a medida que vayan registrando los diferentes usuarios
        user_1=User.objects.create_user(username='agustin',email='agustinO@hotmail.com',password='agustin',last_name='orion',first_name='agustin')
        tel = Telephone.objects.create(number = '427140')
        city = City.objects.get(name='Venado Tuerto', postCode=2600)
        userprofile_1 = UserProfile.objects.create(firstname=user_1.first_name,
                                                     lastname=user_1.last_name,
                                                     email = user_1.email,
                                                     username = user_1.username,
                                                     password = 'agustin',
                                                     telephone = tel,
                                                     city= city,
                                                     user = user_1,
                                                     userType = 'CM',)
        user_2=User.objects.create_user(username='cata',email='ddiaz@hotmail.com',password='daniel',last_name='diaz',first_name='daniel')
        tel = Telephone.objects.create(number = '427141')
        userprofile_2 = UserProfile.objects.create(firstname=user_2.first_name,
                                                     lastname=user_2.last_name,
                                                     email = user_2.email,
                                                     username = user_2.username,
                                                     password = 'daniel',
                                                     telephone = tel,
                                                     city= city,
                                                     user = user_2,
                                                     userType = 'CM',)
        #creo una instancia de Team indicando el nombre del equipo y su capitan
        #el capitan debe ser el mismo usuario que crea el equipo
        equipo = Team.objects.create(name='Central Argentino',captain=usuario.user)
        #agrego los jugadores que formaran parte del equipo
        equipo.players.add(userprofile_1,userprofile_2,usuario)
        equipo.save()

        #el codigo de las lineas anteriores (de la linea 70 a la linea 103) son pasos auxiliares necesarios para listar
        #los equipos con los que cuento(en la view esos pasos no son necesarios ya que no forman parte del proceso
        # de listar equipos, en si).

        #En este caso retornara 1 solo equipo ,que es el total de equipos registrados, si tuviera mas de 1 tambien 
        #me los mostraria

        #codigo principal del test
        Team.objects.all()

    """
    Este test verifica la correcta actualización de un equipo
    """

    def test_teams_update(self):
        usuario = UserProfile.objects.get(username='cris', password='cris')
        #verifico que el usuario tiene permisos de usuario comun
        self.assertEqual(usuario.userType, 'CM')
        #creo por ej n usuarios en forma provisoria solo para poder crear un equipo esto en una view no hace falta
        #pues los usuarios van a ir apareciendo de acuerdo a medida que vayan registrando los diferentes usuarios
        user_1=User.objects.create_user(username='agustin',email='agustinO@hotmail.com',password='agustin',last_name='orion',first_name='agustin')
        tel = Telephone.objects.create(number = '427140')
        city = City.objects.get(name='Venado Tuerto', postCode=2600)
        userprofile_1 = UserProfile.objects.create(firstname=user_1.first_name,
                                                     lastname=user_1.last_name,
                                                     email = user_1.email,
                                                     username = user_1.username,
                                                     password = 'agustin',
                                                     telephone = tel,
                                                     city= city,
                                                     user = user_1,
                                                     userType = 'CM',)
        user_2=User.objects.create_user(username='cata',email='ddiaz@hotmail.com',password='daniel',last_name='diaz',first_name='daniel')
        tel = Telephone.objects.create(number = '427141')
        userprofile_2 = UserProfile.objects.create(firstname=user_2.first_name,
                                                     lastname=user_2.last_name,
                                                     email = user_2.email,
                                                     username = user_2.username,
                                                     password = 'daniel',
                                                     telephone = tel,
                                                     city= city,
                                                     user = user_2,
                                                     userType = 'CM',)
        #creo una instancia de Team indicando el nombre del equipo y su capitan
        #el capitan debe ser el mismo usuario que crea el equipo
        equipo = Team.objects.create(name='Central Argentino',captain=usuario.user)
        #agrego los jugadores que formaran parte del equipo
        equipo.players.add(userprofile_1,userprofile_2,usuario)
        equipo.save()

        #el codigo de las lineas anteriores (de la linea 119 a la linea 152) son pasos auxiliares necesarios para
        #actualizar un determinado equipo 
        #codigo principal del test
        my_team = Team.objects.get(name='Central Argentino',captain=usuario.user)
        self.assertEqual(Team.objects.filter(name='Central Argentino',captain=usuario.user).count(), 1)
        my_team.name='C.A. Central Argentino'
        my_team.save()
        self.assertEqual(Team.objects.filter(name='Central Argentino',captain=usuario.user).count(), 0)
        self.assertEqual(Team.objects.filter(name='C.A. Central Argentino',captain=usuario.user).count(), 1)


    """
    Este test verifica la correcta eliminación de un equipo
    """

    def test_teams_delete(self):
        usuario = UserProfile.objects.get(username='cris', password='cris')
        #verifico que el usuario tiene permisos de usuario comun
        self.assertEqual(usuario.userType, 'CM')
        #creo por ej n usuarios en forma provisoria solo para poder crear un equipo esto en una view no hace falta
        #pues los usuarios van a ir apareciendo de acuerdo a medida que vayan registrando los diferentes usuarios
        user_1=User.objects.create_user(username='agustin',email='agustinO@hotmail.com',password='agustin',last_name='orion',first_name='agustin')
        tel = Telephone.objects.create(number = '427140')
        city = City.objects.get(name='Venado Tuerto', postCode=2600)
        userprofile_1 = UserProfile.objects.create(firstname=user_1.first_name,
                                                     lastname=user_1.last_name,
                                                     email = user_1.email,
                                                     username = user_1.username,
                                                     password = 'agustin',
                                                     telephone = tel,
                                                     city= city,
                                                     user = user_1,
                                                     userType = 'CM',)
        user_2=User.objects.create_user(username='cata',email='ddiaz@hotmail.com',password='daniel',last_name='diaz',first_name='daniel')
        tel = Telephone.objects.create(number = '427141')
        userprofile_2 = UserProfile.objects.create(firstname=user_2.first_name,
                                                     lastname=user_2.last_name,
                                                     email = user_2.email,
                                                     username = user_2.username,
                                                     password = 'daniel',
                                                     telephone = tel,
                                                     city= city,
                                                     user = user_2,
                                                     userType = 'CM',)
        #creo una instancia de Team indicando el nombre del equipo y su capitan
        #el capitan debe ser el mismo usuario que crea el equipo
        equipo = Team.objects.create(name='Central Argentino',captain=usuario.user)
        #agrego los jugadores que formaran parte del equipo
        equipo.players.add(userprofile_1,userprofile_2,usuario)
        equipo.save()

        #el codigo de las lineas anteriores (de la linea 171 a la linea 204) son pasos auxiliares necesarios para
        #eliminacion un determinado equipo 

        #codigo principal del test
        my_team = Team.objects.get(name='Central Argentino',captain=usuario.user)
        self.assertEqual(Team.objects.filter(name='Central Argentino',captain=usuario.user).count(), 1)
        my_team.delete()
        self.assertEqual(Team.objects.filter(name='Central Argentino',captain=usuario.user).count(), 0)

    """
    Este test verifica la busqueda de equipos
    """
    def test_teams_search(self):
        usuario = UserProfile.objects.get(username='cris', password='cris')
        #verifico que el usuario tiene permisos de usuario comun
        self.assertEqual(usuario.userType, 'CM')
        #creo por ej n usuarios en forma provisoria solo para poder crear un equipo esto en una view no hace falta
        #pues los usuarios van a ir apareciendo de acuerdo a medida que vayan registrando los diferentes usuarios
        user_1=User.objects.create_user(username='agustin',email='agustinO@hotmail.com',password='agustin',last_name='orion',first_name='agustin')
        tel = Telephone.objects.create(number = '427140')
        city = City.objects.get(name='Venado Tuerto', postCode=2600)
        userprofile_1 = UserProfile.objects.create(firstname=user_1.first_name,
                                                     lastname=user_1.last_name,
                                                     email = user_1.email,
                                                     username = user_1.username,
                                                     password = 'agustin',
                                                     telephone = tel,
                                                     city= city,
                                                     user = user_1,
                                                     userType = 'CM',)
        user_2=User.objects.create_user(username='cata',email='ddiaz@hotmail.com',password='daniel',last_name='diaz',first_name='daniel')
        tel = Telephone.objects.create(number = '427141')
        userprofile_2 = UserProfile.objects.create(firstname=user_2.first_name,
                                                     lastname=user_2.last_name,
                                                     email = user_2.email,
                                                     username = user_2.username,
                                                     password = 'daniel',
                                                     telephone = tel,
                                                     city= city,
                                                     user = user_2,
                                                     userType = 'CM',)
        #creo una instancia de Team indicando el nombre del equipo y su capitan
        #el capitan debe ser el mismo usuario que crea el equipo
        equipo = Team.objects.create(name='Central Argentino',captain=usuario.user)
        #agrego los jugadores que formaran parte del equipo
        equipo.players.add(userprofile_1,userprofile_2,usuario)
        equipo.save()

        #el codigo de las lineas anteriores (de la linea 171 a la linea 204) son pasos auxiliares necesarios para
        #eliminacion un determinado equipo 

        #codigo principal del test
        equipos = Team.objects.filter(name__contains='Central').distinct()
        #verifico que encontro al menos 1 equipo con el patron de busqueda ingresado
        status = equipos.count() > 0
        self.assertTrue(status)
        #También una busqueda podría devolver 0 resultados
        status = equipos.count() >= 0
        self.assertTrue(status)