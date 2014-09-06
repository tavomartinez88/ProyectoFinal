# -*- encoding: utf-8 -*-
from django.http import HttpResponse #pertenece al módulo django.http

import datetime #biblioteca estándar de python

'''cada función de vista toma como primer argumento un objeto HttpRequest
(llamado gralmente. "request'''
def current_datetime(request): #función de vista
        ''' calcula la fecha/hora actual, como un objeto datetime.datetime y se guarda el resultado en la variable now'''
        #python utiliza tipado dinámico??
        now = datetime.datetime.now()        
        #el %s es reemplazado por el valor de la variable now
        html = "<html><body>It is now: %s.</body></html>" % now
        return HttpResponse(html)

'''cada función de vista toma como primer argumento un objeto HttpRequest
(llamado gralmente. "request'''
def hours_ahead(request, offset):
        #offset = cadena de caracteres capturada por los parentesis en el patron URL
        #convierte la cadena almacenada en offset a un entero
        offset = int(offset)
        #dt = hora actual + hora en Offset. timedelta requiere un parámetro entero.
        dt = datetime.datetime.now() + datetime.timedelta(hours=offset)
        #un %s por cada parametro que quiero mostrar por pantalla
        html = "<html><body>In %s hour(s), it will be %s.</body></html>" % (offset, dt)
        return HttpResponse(html)
