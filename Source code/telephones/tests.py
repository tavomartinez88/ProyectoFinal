from django.test import TestCase





from telephones.models import Telephone,LandLine,CellPhone
#from django.contrib.auth.models import User
# Create your tests here.


class SimpleTest(TestCase):
	def test_es_popular(self):
		landline = LandLine.createLandLine(codeArea="03462", numero="427144")
		
		
	
	




# Create your tests here.
