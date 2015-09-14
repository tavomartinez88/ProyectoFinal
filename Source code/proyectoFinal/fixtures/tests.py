#encoding:utf-8
from django.test import TestCase
from proyectoFinal.citys.models import City
from proyectoFinal.telephones.models import Telephone
from proyectoFinal.teams.models import Team
from proyectoFinal.tournaments.models import Tournament
from proyectoFinal.fixtures.models import Fixture
from proyectoFinal.courts.models import Court
from proyectoFinal.complexes.models import Complex
from proyectoFinal.users.models import UserProfile
from django.contrib.auth.models import User

class FixtureTestCase(TestCase):
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
    												 userType = 'PR',) 

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
        equipo1 = Team.objects.create(name='Central Argentino',captain=user_2)
        #agrego los jugadores que formaran parte del equipo
        equipo1.players.add(userprofile_1,userprofile_2)
        equipo1.save()

        equipo2 = Team.objects.create(name='Newbery F.C',captain=user_1)
        #agrego los jugadores que formaran parte del equipo
        equipo2.players.add(userprofile_1,userprofile_2)
        equipo2.save()

        equipo3 = Team.objects.create(name='Centenario F.C',captain=user_1)
        #agrego los jugadores que formaran parte del equipo
        equipo3.players.add(userprofile_1,userprofile_2)
        equipo3.save()

        Complex.objects.create(name='Oxigeno',streetAddress='Cerrito 1159', roaster=True,buffet=True,lockerRoom=True,user=user_two)

    	torneo = Tournament.objects.create(name='Copa Argentina',complex=Complex.objects.get(name='Oxigeno'))
    	team1 = Team.objects.get(name = 'Central Argentino', captain=User.objects.get(email ='ddiaz@hotmail.com'))
    	team2 = Team.objects.get(name = 'Newbery F.C', captain=User.objects.get(email ='agustinO@hotmail.com'))
    	torneo.teams.add(team1,team2)
    	torneo.save()        

    """
    Este test verifica la correcta creacion de un fixture
    """    
    def test_fixtures_create(self):
    	#defino quien va a registrar el torneo
    	usuario = UserProfile.objects.get(username='cris',password='cris')
    	#verifico que tenga permisos de propietario
    	self.assertEqual(usuario.userType, 'PR')
    	torneo = Tournament.objects.get(name='Copa Argentina',complex=Complex.objects.get(name='Oxigeno'))
    	fixture = Fixture.objects.create(name='Copa Argentina', date='2015-11-16', tournament=torneo)
    	#verifico si se ha creado el fixture
    	self.assertEqual(Fixture.objects.filter(name='Copa Argentina', date='2015-11-16', tournament=torneo).count(), 1)

    """
    Este test verifica la correcta visualizacion de fixtures
    """    
    def test_fixtures_list(self):
    	#defino un usuario,que representa al usuario logueado 
		usuario = UserProfile.objects.get(username='cris',password='cris')
		#verifico que tenga permisos de propietario
		self.assertEqual(usuario.userType, 'PR')
		torneo = Tournament.objects.get(name='Copa Argentina',complex=Complex.objects.get(name='Oxigeno'))
		Fixture.objects.create(name='Copa Argentina', date='2015-11-16', tournament=torneo)
		fixtures = Fixture.objects.filter(tournament=Tournament.objects.filter(complex=Complex.objects.filter(user=usuario.user)))
		usuario = UserProfile.objects.get(username='agustin',password='agustin')
		#verifico que tenga permisos de propietario
		self.assertEqual(usuario.userType, 'CM')
		fixtures = Fixture.objects.filter(tournament=Tournament.objects.filter(inProgress=True))


		
    """
    Este test verifica la correcta eliminacion de un fixture
    """    
    def test_fixtures_delete(self):
    	#defino un usuario,que representa al usuario logueado 
    	usuario = UserProfile.objects.get(username='cris',password='cris')
    	#verifico que tenga permisos de propietario
    	self.assertEqual(usuario.userType, 'PR')
    	torneo = Tournament.objects.get(name='Copa Argentina',complex=Complex.objects.get(name='Oxigeno'))
    	fixture = Fixture.objects.create(name='Copa Argentina', date='2015-11-16', tournament=torneo)
    	fixture_for_delete = Fixture.objects.get(name='Copa Argentina', date='2015-11-16', tournament=torneo)
    	self.assertEqual(Fixture.objects.filter(name='Copa Argentina', date='2015-11-16', tournament=torneo).count(), 1)
    	self.assertTrue(fixture_for_delete.tournament.complex.user == usuario.user)
    	fixture_for_delete.delete()
    	self.assertEqual(Fixture.objects.filter(name='Copa Argentina', date='2015-11-16', tournament=torneo).count(), 0)


    """
    Este test verifica la correcta actualizacion de un fixture
    """    
    def test_fixtures_update(self):
    	#defino un usuario,que representa al usuario logueado 
    	usuario = UserProfile.objects.get(username='cris',password='cris')
    	#verifico que tenga permisos de propietario
    	self.assertEqual(usuario.userType, 'PR')
    	torneo = Tournament.objects.get(name='Copa Argentina',complex=Complex.objects.get(name='Oxigeno'))
    	fixture = Fixture.objects.create(name='Copa Argentina', date='2015-11-16', tournament=torneo)

    	self.assertEqual(Fixture.objects.filter(name='Copa Argentina', date='2015-11-16', tournament=torneo).count(), 1)
    	fixture_for_update = Fixture.objects.get(name='Copa Argentina', date='2015-11-16', tournament=torneo)    	
    	self.assertTrue(fixture_for_update.tournament.complex.user == usuario.user)
    	
    	fixture_for_update.name = 'Copa República Argentina'
    	fixture_for_update.save()
    	self.assertEqual(Fixture.objects.filter(name='Copa Argentina', date='2015-11-16', tournament=torneo).count(), 0)
    	self.assertEqual(Fixture.objects.filter(name='Copa República Argentina', date='2015-11-16', tournament=torneo).count(), 1)


    """
    Este test verifica la correcta busqueda de fixtures
    """    
    def test_fixtures_search(self):
    	torneo = Tournament.objects.get(name='Copa Argentina',complex=Complex.objects.get(name='Oxigeno'))
    	fixture = Fixture.objects.create(name='Copa Argentina', date='2015-11-16', tournament=torneo)
    	fix = Fixture.objects.filter(date='2015-11-16').distinct()
    	self.assertTrue(fix>=0)
