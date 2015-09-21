#encoding:utf-8
from django.test import TestCase
from proyectoFinal.citys.models import City
from proyectoFinal.telephones.models import Telephone
from proyectoFinal.courts.models import Court
from proyectoFinal.complexes.models import Complex
from proyectoFinal.reservations.models import Reservation
from proyectoFinal.users.models import UserProfile
from django.contrib.auth.models import User
from datetime import date


class ReservationTestCase(TestCase):
    def setUp(self):
    	ciudad = City.objects.create(name='Venado Tuerto', postCode=2600)
    	tel = Telephone.objects.create(number = '154864587')
    	user_one=User.objects.create_user(username='tavo',email='gmartinezgranella@gmail.com',last_name='martinez',first_name='gustavo')
    	userprofile_one = UserProfile.objects.create(firstname=user_one.first_name,
    												 lastname=user_one.last_name,
    												 email = user_one.email,
    												 username = user_one.username,
    												 password = 'tavo',
    												 telephone = tel,
    												 city= ciudad,
    												 user = user_one,
    												 userType = 'PR',)

    	user_two=User.objects.create_user(username='cris',email='cris_09@hotmail.com',last_name='martinez',first_name='cristian')
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

        user_third=User.objects.create_user(username='ariel',email='ariel_09@hotmail.com',last_name='martinez',first_name='ariel')
        tel3 = Telephone.objects.create(number = '427142')
        userprofile_third = UserProfile.objects.create(firstname=user_third.first_name,
                                                     lastname=user_third.last_name,
                                                     email = user_third.email,
                                                     username = user_third.username,
                                                     password = 'ariel',
                                                     telephone = tel3,
                                                     city= ciudad,
                                                     user = user_third,
                                                     userType = 'CM',)                                                         	

    	Complex.objects.create(name='Oxigeno',streetAddress='Cerrito 1159', roaster=True,buffet=True,lockerRoom=True,user=userprofile_one.user)
    	court1 = Court.objects.create(artificial_light=True, lawnType='Futsal', soccerType='Futbol 5', complex=Complex.objects.get(name='Oxigeno'), name='1A')
    	court2 = Court.objects.create(artificial_light=True, lawnType='Futsal', soccerType='Futbol 5', complex=Complex.objects.get(name='Oxigeno'), name='2A')
    	court3 = Court.objects.create(artificial_light=True, lawnType='Futsal', soccerType='Futbol 5', complex=Complex.objects.get(name='Oxigeno'), name='3A')
        Reservation.objects.create(date=date(2015,12,11),hour=21,minutes=30,user=userprofile_third,court=court2)
        

    """
    Este test verifica la correcta creacion de una reservación asociada a un usuario y a un complejo
    """
    def test_reservations_create(self):
    	#---------para un usuario 'PR' como usuario logueado
    	#voy a realizar la correspondiente verificacion de una reserva para un ususario no suspendido
    	usuario_logued = UserProfile.objects.get(username='tavo', password='tavo')
    	#verifico que el usuario tiene permisos de propietario
    	self.assertEqual(usuario_logued.userType, 'PR')
    	#datos de la reserva
    	cancha = Court.objects.get(name="1A")
    	usuario = UserProfile.objects.get(username='cris',password='cris')
    	fecha_reserva = date(2015,12,25)
    	hora_reserva = 21
    	minutos_reserva = 30
    	#verifico que el num de minutos es correcto
    	self.assertTrue(minutos_reserva==00 or minutos_reserva==30)
    	#verifico si esta suspendido
    	self.assertTrue(usuario.suspended==False)
    	#verifico que no tiene 3 o mas reservaciones en las que no asistió
    	self.assertTrue(Reservation.objects.filter(user=usuario,attended=False,verificated=False).count()<=3)
    	#verifico que no hay ninguna reserva con los mismos datos
    	self.assertTrue(Reservation.objects.filter(date=fecha_reserva,hour=hora_reserva,minutes=minutos_reserva,court=cancha).count()==0)
    	reservacion = Reservation.objects.create(date='2015-12-25',hour=21,minutes=30,user=usuario,court=cancha)
    	#verifico que ahora existe 1 reservacion con los datos sumisnistrados
    	self.assertTrue(Reservation.objects.filter(date=fecha_reserva,hour=hora_reserva,minutes=minutos_reserva,court=cancha).count()==1)
    	#-----------------------------------------------
    	#verifico ahora para un usuario suspendido
    	#suspendo temporalmente al usuario (esto es auxiliar)
    	usuario.suspended=True
    	usuario.dateSuspended=date(2015,8,15)
    	usuario.save()
		#utilizo la misma cancha
    	fecha_reserva = date(2015,12,12)
    	hora_reserva = 16
    	minutos_reserva = 30
    	#verifico que los datos sean correctos
    	self.assertTrue(minutos_reserva==00 or minutos_reserva==30)
    	self.assertTrue(usuario.suspended==True)
    	dias = date.today()-usuario.dateSuspended
    	#verifico si el usuario ya cumplio con la suspensión, si es asi quito la suspension al usuario
    	self.assertTrue(dias.days>=30)
    	usuario.suspended=False
    	usuario.save()
    	#verifico si el usuario tiene mas de 3 reservaciones no asistidas,donde cada reservación no debe haber sido 
    	#verificada antes.
    	self.assertTrue(Reservation.objects.filter(user=usuario,attended=False,verificated=False).count()<=3)
    	#verifico si no existe ninguna reservacion con la cancha, dia y horario indicado.
    	self.assertTrue(Reservation.objects.filter(date=fecha_reserva,hour=hora_reserva,minutes=minutos_reserva,court=cancha).count()==0)
    	#creo la reservación y vuelvo a verificar que ahora si existe una reservacion
    	reservacion = Reservation.objects.create(date=fecha_reserva,hour=hora_reserva,minutes=minutos_reserva,user=usuario,court=cancha)
    	self.assertTrue(Reservation.objects.filter(date=fecha_reserva,hour=hora_reserva,minutes=minutos_reserva,court=cancha).count()==1)
    	#--------------------------------------------------
    	#--------para un usuario 'CM' como usuario logueado
    	#primero pruebo para un usuario que no esta suspendido
    	usuario_logued = UserProfile.objects.get(username='cris',password='cris')
    	self.assertTrue(usuario_logued.userType=='CM')
    	self.assertTrue(usuario_logued.suspended==False)
    	self.assertTrue(Reservation.objects.filter(user=usuario_logued,attended=False,verificated=False).count()<=3)
    	fecha_reserva=date(2015,12,13)
    	hora_reserva=20
    	minutos_reserva=30
    	cancha=Court.objects.get(name='2A')
    	self.assertTrue(Reservation.objects.filter(date=fecha_reserva,hour=hora_reserva,minutes=minutos_reserva,court=cancha).count()==0)
    	reservacion = Reservation.objects.create(date=fecha_reserva,hour=hora_reserva,minutes=minutos_reserva,user=usuario_logued,court=cancha)
    	self.assertTrue(Reservation.objects.filter(date=fecha_reserva,hour=hora_reserva,minutes=minutos_reserva,court=cancha).count()==1)
		#ahora pruebo para cuando esta suspendido
    	usuario_logued.suspended=True
    	usuario_logued.dateSuspended=date(2015,8,15)
    	usuario_logued.save()
		#utilizo la misma cancha
    	fecha_reserva = date(2015,12,12)
    	hora_reserva = 16
    	minutos_reserva = 30
    	#verifico que los datos sean correctos
    	self.assertTrue(minutos_reserva==00 or minutos_reserva==30)
    	self.assertTrue(usuario_logued.suspended==True)
    	dias = date.today()-usuario_logued.dateSuspended
    	#verifico si el usuario ya cumplio con la suspensión, si es asi quito la suspension al usuario
    	self.assertTrue(dias.days>=30)
    	usuario_logued.suspended=False
    	usuario_logued.save()
    	#verifico si el usuario tiene mas de 3 reservaciones no asistidas,donde cada reservación no debe haber sido 
    	#verificada antes.
    	self.assertTrue(Reservation.objects.filter(user=usuario_logued,attended=False,verificated=False).count()<=3)
    	#verifico si no existe ninguna reservacion con la cancha, dia y horario indicado.
    	self.assertTrue(Reservation.objects.filter(date=fecha_reserva,hour=hora_reserva,minutes=minutos_reserva,court=cancha).count()==0)
    	#creo la reservación y vuelvo a verificar que ahora si existe una reservacion
    	reservacion = Reservation.objects.create(date=fecha_reserva,hour=hora_reserva,minutes=minutos_reserva,user=usuario_logued,court=cancha)
    	self.assertTrue(Reservation.objects.filter(date=fecha_reserva,hour=hora_reserva,minutes=minutos_reserva,court=cancha).count()==1)

    def test_reservations_list(self):
        #solo se mostraran si el usuario esta logueado, de lo contrario redireccionará para que pueda loguearse
        #si el usuario logueado es un usuario con permisos de usuario común
        usuario_logued = UserProfile.objects.get(username='ariel',password='ariel')
        self.assertTrue(Reservation.objects.filter(user=usuario_logued).count()==1)
        #si el usuario logueado es un usuario con permisos de usuario propietario
        usuario_logued = UserProfile.objects.get(username='tavo',password='tavo')
        Reservation.objects.create(date=date(2015,12,21),hour=21,minutes=30,user=UserProfile.objects.get(username='cris',password='cris'),court=Court.objects.get(name='1A'))
        Reservation.objects.create(date=date(2015,12,21),hour=21,minutes=30,user=UserProfile.objects.get(username='cris',password='cris'),court=Court.objects.get(name='2A'))
        Reservation.objects.create(date=date(2015,12,21),hour=21,minutes=30,user=UserProfile.objects.get(username='cris',password='cris'),court=Court.objects.get(name='3A'))
        self.assertTrue(Reservation.objects.filter(court=Court.objects.filter(complex=Complex.objects.filter(user=usuario_logued.user))).count()==4)


    def test_reservations_update(self):
        #solo se podrá actualizar si el usuario esta logueado y es un usuario propietario
        usuario_logued = UserProfile.objects.get(username='tavo',password='tavo')
        self.assertTrue(usuario_logued.userType=='PR')
        reserva = Reservation.objects.get(date=date(2015,12,11),hour=21,minutes=30,user=UserProfile.objects.get(username='ariel',password='ariel'),court=Court.objects.get(name='2A'))
        self.assertTrue(reserva.attended==False)
        reserva.attended=True
        reserva.save()
        self.assertTrue(reserva.attended==True)

    def test_reservations_cancel(self):
        #solo se podrá actualizar si el usuario esta logueado y es un usuario propietario
        usuario_logued = UserProfile.objects.get(username='tavo',password='tavo')
        self.assertTrue(usuario_logued.userType=='PR')
        reserva = Reservation.objects.get(date=date(2015,12,11),hour=21,minutes=30,user=UserProfile.objects.get(username='ariel',password='ariel'),court=Court.objects.get(name='2A'))
        fecha_actual = date.today()
        self.assertTrue(fecha_actual<=reserva.date)
        reserva.delete()
        c_reserva = Reservation.objects.filter(date=date(2015,12,11),hour=21,minutes=30,user=UserProfile.objects.get(username='ariel',password='ariel'),court=Court.objects.get(name='2A'))
        self.assertTrue(c_reserva.count()==0)