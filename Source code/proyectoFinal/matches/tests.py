#encoding:utf-8
from django.test import TestCase
from proyectoFinal.citys.models import City
from proyectoFinal.telephones.models import Telephone
from proyectoFinal.teams.models import Team
from proyectoFinal.tournaments.models import Tournament
from proyectoFinal.fixtures.models import Fixture
from proyectoFinal.matches.models import Match
from proyectoFinal.courts.models import Court
from proyectoFinal.complexes.models import Complex
from proyectoFinal.users.models import UserProfile
from django.contrib.auth.models import User
import datetime

class MatchTestCase(TestCase):
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

        Fixture.objects.create(name='Copa Argentina', date='2015-11-16', tournament=torneo)



    """
    Este test verifica la correcta creacion de un partido
    """    
    def test_matches_create(self):
    	#defino quien va a registrar el torneo
    	usuario = UserProfile.objects.get(username='cris',password='cris')
    	#verifico que tenga permisos de propietario
    	self.assertEqual(usuario.userType, 'PR')
        fixture = Fixture.objects.get(name='Copa Argentina', date='2015-11-16')
        #verifico que el fixture es de propiedad del usuario que ontenta registrar un nuevo partido
        self.assertTrue(fixture.tournament.complex.user == usuario.user)
        equipo1=Team.objects.get(name='Central Argentino')
        equipo2=Team.objects.get(name='Centenario F.C')
        partido = Match.objects.create(day=datetime.date(2015, 11, 16),hour=16,minutes=30,teamlocal=equipo1,teamVisitant=equipo2,fixture=fixture)
        #verifico que la fecha del partido es igual o mayor al del comienzo del fixture
        self.assertTrue(partido.day >= fixture.date)
        #verifico que en un mismo partido, los equipos involucrados sean distintos entre si
        self.assertTrue(equipo1 != equipo2)


    """
    Este test verifica la correcta eliminacion de un partido
    """    
    def test_matches_delete(self):
        #defino quien va a registrar el torneo
        usuario = UserProfile.objects.get(username='cris',password='cris')
        #verifico que tenga permisos de propietario
        self.assertEqual(usuario.userType, 'PR')
        fixture = Fixture.objects.get(name='Copa Argentina', date='2015-11-16')
        #verifico que el fixture es de propiedad del usuario que ontenta registrar un nuevo partido
        self.assertTrue(fixture.tournament.complex.user == usuario.user)
        equipo1=Team.objects.get(name='Central Argentino')
        equipo2=Team.objects.get(name='Centenario F.C')
        partido = Match.objects.create(day=datetime.date(2015, 11, 16),hour=16,minutes=30,teamlocal=equipo1,teamVisitant=equipo2,fixture=fixture)
        #verifico que la fecha del partido es igual o mayor al del comienzo del fixture
        self.assertTrue(partido.day >= fixture.date)
        #verifico que en un mismo partido, los equipos involucrados sean distintos entre si
        self.assertTrue(equipo1 != equipo2)
        # verifico que cuento con el partido del dia 16/11/2015 a las 16:30 entre el equipo1 y el equipo2
        self.assertTrue(Match.objects.filter(day=datetime.date(2015, 11, 16),hour=16,minutes=30,teamlocal=equipo1,teamVisitant=equipo2,fixture=fixture).count()==1)
        partido.delete()
        # verifico que ya no cuento con el partido del dia 16/11/2015 a las 16:30 entre el equipo1 y el equipo2
        self.assertFalse(Match.objects.filter(day=datetime.date(2015, 11, 16),hour=16,minutes=30,teamlocal=equipo1,teamVisitant=equipo2,fixture=fixture).count()==1)

    """
    Este test verifica la correcta actualizacion de un partido
    """    
    def test_matches_update(self):
        #defino quien va a registrar el torneo
        usuario = UserProfile.objects.get(username='cris',password='cris')
        #verifico que tenga permisos de propietario
        self.assertEqual(usuario.userType, 'PR')
        fixture = Fixture.objects.get(name='Copa Argentina', date='2015-11-16')
        #verifico que el fixture es de propiedad del usuario que ontenta registrar un nuevo partido
        self.assertTrue(fixture.tournament.complex.user == usuario.user)
        equipo1=Team.objects.get(name='Central Argentino')
        equipo2=Team.objects.get(name='Centenario F.C')
        partido = Match.objects.create(day=datetime.date(2015, 11, 16),hour=16,minutes=30,teamlocal=equipo1,teamVisitant=equipo2,fixture=fixture)
        #verifico que la fecha del partido es igual o mayor al del comienzo del fixture
        self.assertTrue(partido.day >= fixture.date)
        #verifico que en un mismo partido, los equipos involucrados sean distintos entre si
        self.assertTrue(equipo1 != equipo2)
        # verifico que cuento con el partido del dia 16/11/2015 a las 16:30 entre el equipo1 y el equipo2
        self.assertTrue(Match.objects.filter(day=datetime.date(2015, 11, 16),hour=16,minutes=30,teamlocal=equipo1,teamVisitant=equipo2,fixture=fixture).count()==1)
        


        #codigo principal del test
        partido.scoreLocal = 3
        partido.scoreVisit = 3
        partido.save()
        self.assertEqual(partido.scoreLocal, 3)
        self.assertEqual(partido.scoreVisit, 3)


    """
    Este test verifica la correcta de listar partidos
    """    
    def test_matches_list(self):
        #sii el usuario ha sido logueado mostrara los partidos 
        #necesito un determinado fixture para saber que partidos debo listar
        usuario = UserProfile.objects.get(username='cris',password='cris')
        fixture = Fixture.objects.get(name='Copa Argentina', date='2015-11-16')
        self.assertTrue(fixture.tournament.complex.user == usuario.user)
        equipo1=Team.objects.get(name='Central Argentino')
        equipo2=Team.objects.get(name='Centenario F.C')
        partido1 = Match.objects.create(day=datetime.date(2015, 11, 16),hour=16,minutes=30,teamlocal=equipo1,teamVisitant=equipo2,fixture=fixture)
        #verifico que la fecha del partido es igual o mayor al del comienzo del fixture
        self.assertTrue(partido1.day >= fixture.date)
        #verifico que en un mismo partido, los equipos involucrados sean distintos entre si
        self.assertTrue(equipo1 != equipo2) 
        self.assertTrue(fixture.tournament.complex.user == usuario.user)
        equipo1=Team.objects.get(name='Central Argentino')
        equipo2=Team.objects.get(name='Centenario F.C')
        partido2 = Match.objects.create(day=datetime.date(2015, 11, 26),hour=16,minutes=30,teamlocal=equipo2,teamVisitant=equipo1,fixture=fixture)
        #verifico que la fecha del partido es igual o mayor al del comienzo del fixture
        self.assertTrue(partido2.day >= fixture.date)
        #verifico que en un mismo partido, los equipos involucrados sean distintos entre si
        self.assertTrue(equipo1 != equipo2)               
        Match.objects.filter(fixture=fixture).count()

    """
    Este test verifica la correcta de buscar partidos
    """
    def test_matches_search(self):
        #sii el usuario ha sido logueado mostrara los partidos 
        #necesito un determinado fixture para saber que partidos debo listar
        usuario = UserProfile.objects.get(username='cris',password='cris')
        fixture = Fixture.objects.get(name='Copa Argentina', date='2015-11-16')
        self.assertTrue(fixture.tournament.complex.user == usuario.user)
        equipo1=Team.objects.get(name='Central Argentino')
        equipo2=Team.objects.get(name='Centenario F.C')
        partido1 = Match.objects.create(day=datetime.date(2015, 11, 16),hour=16,minutes=30,teamlocal=equipo1,teamVisitant=equipo2,fixture=fixture)
        #verifico que la fecha del partido es igual o mayor al del comienzo del fixture
        self.assertTrue(partido1.day >= fixture.date)
        #verifico que en un mismo partido, los equipos involucrados sean distintos entre si
        self.assertTrue(equipo1 != equipo2)

        #codigo principal del test
        partidos = Match.objects.filter(day=datetime.date(2015, 11, 16))
        self.assertTrue(partidos.count()>=0)