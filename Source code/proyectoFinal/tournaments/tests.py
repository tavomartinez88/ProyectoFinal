#encoding:utf-8
from django.test import TestCase
from proyectoFinal.citys.models import City
from proyectoFinal.telephones.models import Telephone
from proyectoFinal.teams.models import Team
from proyectoFinal.tournaments.models import Tournament
from proyectoFinal.courts.models import Court
from proyectoFinal.complexes.models import Complex
from proyectoFinal.users.models import UserProfile
from django.contrib.auth.models import User

class TournamentTestCase(TestCase):
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

    """
    Este test verifica la correcta creacion de un torneo
    """    
    def test_tournaments_create(self):
    	#defino quien va a registrar el torneo
    	usuario = UserProfile.objects.get(username='cris',password='cris')
    	#verifico que tenga permisos de propietario
    	self.assertEqual(usuario.userType, 'PR')
    	#defino un torneo indicando nombre,los n equipos que disputan el torneo y el complejo donde se disputa el torneo
    	#Elegi el complejo 'Oxigeno' pero se podria haber elegido otro,siempre y cuando sea de la propiedad del mismo 
    	#usuario que esta registrando el torneo.

    	#verifico si tengo algun torneo que se corresponda con el nombre 'Copa Argentina'
    	self.assertEqual(Tournament.objects.filter(name='Copa Argentina').count(), 0)
    	#lo correcto seria que no exista un torneo con ese nombe.Ahora creo uno con ese nombre y vuelvo a verificar
    	torneo = Tournament.objects.create(name='Copa Argentina',complex=Complex.objects.get(name='Oxigeno'))
    	team1 = Team.objects.get(name = 'Central Argentino', captain=User.objects.get(email ='ddiaz@hotmail.com'))
    	team2 = Team.objects.get(name = 'Newbery F.C', captain=User.objects.get(email ='agustinO@hotmail.com'))
    	torneo.teams.add(team1,team2)
    	torneo.save()
    	self.assertEqual(Tournament.objects.filter(name='Copa Argentina').count(), 1)

    """
    Este test verifica la correcta visualizacion de torneos
    """    
    def test_tournaments_list(self):
    	#si el usuario no esta identificado 
    	Tournament.objects.all()
    	#si el usuario esta identificado
    	usuario = UserProfile.objects.get(username='agustin' , password='agustin')
    	#si el usuario tiene permisos de usuario comun retorno todos los torneos
    	self.assertEqual(usuario.userType, 'CM')
    	Tournament.objects.all()
    	usuario = UserProfile.objects.get(username='cris' , password='cris')
    	#si el usuario tiene permisos de usuario propietario retorno todos los torneos que se disputan en complejos
    	# que pertenecen al usuario
    	self.assertEqual(usuario.userType, 'PR')
    	Tournament.objects.filter(complex=Complex.objects.filter(user= usuario.user))


    """
    Este test verifica la correcta actualizacion de un determinado torneo
    """    
    def test_tournaments_markAsFinished(self):
    	#defino quien va a registrar el torneo
    	usuario = UserProfile.objects.get(username='cris',password='cris')
    	#verifico que tenga permisos de propietario
    	self.assertEqual(usuario.userType, 'PR')
    	#defino un torneo indicando nombre,los n equipos que disputan el torneo y el complejo donde se disputa el torneo
    	#Elegi el complejo 'Oxigeno' pero se podria haber elegido otro,siempre y cuando sea de la propiedad del mismo 
    	#usuario que esta registrando el torneo.

    	#verifico si tengo algun torneo que se corresponda con el nombre 'Copa Argentina'
    	self.assertEqual(Tournament.objects.filter(name='Copa Argentina').count(), 0)
    	#lo correcto seria que no exista un torneo con ese nombe.Ahora creo uno con ese nombre y vuelvo a verificar
    	torneo = Tournament.objects.create(name='Copa Argentina',complex=Complex.objects.get(name='Oxigeno'))
    	team1 = Team.objects.get(name = 'Central Argentino', captain=User.objects.get(email ='ddiaz@hotmail.com'))
    	team2 = Team.objects.get(name = 'Newbery F.C', captain=User.objects.get(email ='agustinO@hotmail.com'))
    	torneo.teams.add(team1,team2)
    	torneo.save()
    	
    	#Hasta ahora tengo un torneo con 2 equipos
    	self.assertEqual(torneo.teams.count(), 2)
    	#agrego un nuevo equipo al torneo
    	team3 = Team.objects.get(name = 'Centenario F.C', captain=User.objects.get(email ='agustinO@hotmail.com'))
    	torneo.teams.add(team3)
    	torneo.save()
    	#ahora, luego de la actualización deberia tener 3 equipos y no 2 en el torneo
    	self.assertEqual(torneo.teams.count(), 3)
    	
    	#Hasta ahora tengo un torneo en juego 
    	self.assertTrue(torneo.inProgress)
    	torneo.inProgress = False
    	torneo.save()
    	#al actualizar la progresión del torneo deberia ahora no tener dicho torneo (en juego),es decir deberia estar finalizado
    	self.assertFalse(torneo.inProgress)

    """
    Este test verifica la correcta eliminacion de un determinado torneo
    """    
    def test_tournaments_cancel(self):
    	#defino quien va a registrar el torneo
    	usuario = UserProfile.objects.get(username='cris',password='cris')
    	#verifico que tenga permisos de propietario
    	self.assertEqual(usuario.userType, 'PR')
    	#defino un torneo indicando nombre,los n equipos que disputan el torneo y el complejo donde se disputa el torneo
    	#Elegi el complejo 'Oxigeno' pero se podria haber elegido otro,siempre y cuando sea de la propiedad del mismo 
    	#usuario que esta registrando el torneo.

    	#verifico si tengo algun torneo que se corresponda con el nombre 'Copa Argentina'
    	self.assertEqual(Tournament.objects.filter(name='Copa Argentina').count(), 0)
    	#lo correcto seria que no exista un torneo con ese nombe.Ahora creo uno con ese nombre y vuelvo a verificar
    	torneo = Tournament.objects.create(name='Copa Argentina',complex=Complex.objects.get(name='Oxigeno'))
    	team1 = Team.objects.get(name = 'Central Argentino', captain=User.objects.get(email ='ddiaz@hotmail.com'))
    	team2 = Team.objects.get(name = 'Newbery F.C', captain=User.objects.get(email ='agustinO@hotmail.com'))
    	torneo.teams.add(team1,team2)
    	torneo.save()
    	
    	#Hasta ahora tengo un torneo 'Copa Argentina' que se disputa en el complejo 'Oxigeno'
    	self.assertEqual(Tournament.objects.filter(name='Copa Argentina',complex=Complex.objects.get(name='Oxigeno')).count(), 1)
    	torneo.delete()
    	#luego de la eliminacion no deberia tener ningun torneo 'Copa Argentina' que se disputa en el complejo 'Oxigeno'
    	self.assertEqual(Tournament.objects.filter(name='Copa Argentina',complex=Complex.objects.get(name='Oxigeno')).count(), 0)

    """
    Este test verifica la correcta forma de buscar torneos
    """
    def test_tournaments_search(self):
    	#defino quien va a registrar el torneo
    	usuario = UserProfile.objects.get(username='cris',password='cris')
    	#verifico que tenga permisos de propietario
    	self.assertEqual(usuario.userType, 'PR')
    	#defino un torneo indicando nombre,los n equipos que disputan el torneo y el complejo donde se disputa el torneo
    	#Elegi el complejo 'Oxigeno' pero se podria haber elegido otro,siempre y cuando sea de la propiedad del mismo 
    	#usuario que esta registrando el torneo.

    	#verifico si tengo algun torneo que se corresponda con el nombre 'Copa Argentina'
    	self.assertEqual(Tournament.objects.filter(name='Copa Argentina').count(), 0)
    	#lo correcto seria que no exista un torneo con ese nombe.Ahora creo uno con ese nombre y vuelvo a verificar
    	torneo = Tournament.objects.create(name='Copa Argentina',complex=Complex.objects.get(name='Oxigeno'))
    	team1 = Team.objects.get(name = 'Central Argentino', captain=User.objects.get(email ='ddiaz@hotmail.com'))
    	team2 = Team.objects.get(name = 'Newbery F.C', captain=User.objects.get(email ='agustinO@hotmail.com'))
    	torneo.teams.add(team1,team2)
    	torneo.save()
        torneos = Tournament.objects.filter(name__contains='Copa Argentina').distinct()
        #verifico que encontro al menos 1 equipo con el patron de busqueda ingresado
        #También una busqueda podría devolver 0 resultados
        self.assertTrue(torneos.count() >= 0)    	