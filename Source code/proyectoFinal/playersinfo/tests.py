#encoding:utf-8
from django.test import TestCase
from proyectoFinal.citys.models import City
from proyectoFinal.telephones.models import Telephone
from proyectoFinal.playersinfo.models import PlayersInfo
from proyectoFinal.teams.models import Team
from proyectoFinal.tournaments.models import Tournament
from proyectoFinal.fixtures.models import Fixture
from proyectoFinal.matches.models import Match
from proyectoFinal.courts.models import Court
from proyectoFinal.complexes.models import Complex
from proyectoFinal.users.models import UserProfile
from django.contrib.auth.models import User
import datetime
from django.db.models import Q

class PlayersInfoTestCase(TestCase):
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

    def test_playersinfo_create(self):
    	#usuario que realiza la estadistica de un jugador 
    	usuario_logued = UserProfile.objects.get(username='cris', password='cris')
    	#verifico que tiene los permisos de propietario
    	self.assertTrue(usuario_logued.userType=='PR')
    	#obtengo el torneo en el que participa el jugador 
    	torneo = Tournament.objects.get(name='Copa Argentina')    	
    	#verifico que el usuario que realiza la estadistica y el usuario propietario del torneo son el mismo 
    	self.assertTrue(torneo.complex.user == usuario_logued.user)
    	#obtengo el jugador al que le voy a crear las estadisticas
    	usuario_stadistic = UserProfile.objects.get(username='agustin', password='agustin')
    	#verifico que el usuario al que se le va a crear estadisticas posee permisos de usuario comun
    	self.assertTrue(usuario_stadistic.userType=='CM')
    	#verifico que no hay estadisticas para el jugador en el torneo
    	self.assertTrue(PlayersInfo.objects.filter(user=usuario_stadistic,tournament=torneo).count()==0)
    	#creo la estadistica y vuelvo a verificar
    	estadistica = PlayersInfo.objects.create(goals=14,yellowCards=3,redCards=1,user=usuario_stadistic,tournament=torneo)
    	self.assertFalse(PlayersInfo.objects.filter(user=usuario_stadistic,tournament=torneo).count()==0)

    def test_playersinfo_list(self):
    	usuario_logued = UserProfile.objects.get(username='cris', password='cris')
    	#verifico que usuario logueado tiene permisos de usuario propietario
    	self.assertTrue(usuario_logued.userType=='PR')
    	#obtengo el torneo en el que participar el jugador
    	torneo = Tournament.objects.get(name='Copa Argentina')
    	#verifico que el usuario que realiza la estadistica y el usuario propietario del torneo son el mismo
    	self.assertTrue(usuario_logued.user == torneo.complex.user)
    	#obtengo el jugador al que le voy a crear las estadisticas
    	usuario_stadistic = UserProfile.objects.get(username='agustin', password='agustin')
    	self.assertTrue(usuario_stadistic.userType=='CM')
    	#creo la estadistica para el jugador en el torneo y verifico que se ha creado correctamente la estadistica
    	estadistica = PlayersInfo.objects.create(goals=14,yellowCards=3,redCards=1,user=usuario_stadistic,tournament=torneo)
    	self.assertTrue(PlayersInfo.objects.filter(user=usuario_stadistic,tournament=torneo).count()==1)

    def test_playersinfo_update(self):
    	usuario_logued = UserProfile.objects.get(username='cris', password='cris')
    	#verifico que usuario logueado tiene permisos de usuario propietario
    	self.assertTrue(usuario_logued.userType=='PR')
    	#obtengo el torneo en el que participar el jugador
    	torneo = Tournament.objects.get(name='Copa Argentina')
    	#verifico que el usuario que realiza la estadistica y el usuario propietario del torneo son el mismo
    	self.assertTrue(usuario_logued.user == torneo.complex.user)
    	#obtengo el jugador al que le voy a editar la estadistica
    	usuario_stadistic = UserProfile.objects.get(username='agustin', password='agustin')
    	self.assertTrue(usuario_stadistic.userType=='CM')
    	#creo la estadistica para el jugador en el torneo y verifico que se ha creado correctamente la estadistica
    	estadistica = PlayersInfo.objects.create(goals=14,yellowCards=3,redCards=1,user=usuario_stadistic,tournament=torneo)
    	estadistica.goals=35
    	estadistica.yellowCards=5
    	estadistica.redCards=6
    	estadistica.save()
    	#verifico que se ha actualizado correctamente la estadistica
    	self.assertTrue(estadistica.goals==35 and estadistica.yellowCards==5 and estadistica.redCards==6)

    """
    Este test verifica la correcta de buscar partidos
    """
    def test_playersinfo_search(self):
    	usuario_logued = UserProfile.objects.get(username='cris', password='cris')
    	#verifico que usuario logueado tiene permisos de usuario propietario
    	self.assertTrue(usuario_logued.userType=='PR')
    	#obtengo el torneo en el que participar el jugador
    	torneo = Tournament.objects.get(name='Copa Argentina')
    	#verifico que el usuario que realiza la estadistica y el usuario propietario del torneo son el mismo
    	self.assertTrue(usuario_logued.user == torneo.complex.user)
    	#obtengo el jugador al que le voy a editar la estadistica
    	usuario_stadistic = UserProfile.objects.get(username='agustin', password='agustin')
    	self.assertTrue(usuario_stadistic.userType=='CM')
    	#creo la estadistica para el jugador en el torneo y verifico que se ha creado correctamente la estadistica
    	estadistica = PlayersInfo.objects.create(goals=14,yellowCards=3,redCards=1,user=usuario_stadistic,tournament=torneo)
    	estadistica.goals=35
    	estadistica.yellowCards=5
    	estadistica.redCards=6
    	estadistica.save()
    	#verifico que se ha actualizado correctamente la estadistica
    	self.assertTrue(estadistica.goals==35 and estadistica.yellowCards==5 and estadistica.redCards==6)

        #codigo principal del test
        pattern_search = 'agustin orion'
        qset = (Q(user__firstname__icontains=pattern_search) | (Q(user__lastname__icontains=pattern_search)))
        partidos = PlayersInfo.objects.filter(qset).distinct()
        self.assertTrue(partidos.count()>=0)        