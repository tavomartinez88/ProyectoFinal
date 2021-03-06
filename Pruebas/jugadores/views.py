from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse
from jugadores.models import jugadores
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from django import forms

def search_player(request):
   query = request.GET.get('q', '')
   if query:
      qset = (Q(nombre__icontains=query) |
      Q(apellido__icontains=query) |
      Q(dni__contains=query))
      results = jugadores.objects.filter(qset).distinct()
   else:
      results = []
   return render_to_response("search_player.html", {"results": results,"query": query})

def registrar_jugador(request):
    nombre = request.GET.get('nombre', '')
    apellido = request.GET.get('apellido', '')
    dni = request.GET.get('dni', 0)
    email = request.GET.get('email', '')
    direccion = request.GET.get('direccion', '')
    telefono1 = request.GET.get('telefono1', '')
    telefono2 = request.GET.get('telefono2', '')
    username = request.GET.get('username', '')
    password = request.GET.get('password', '')
    res = jugadores(nombre=nombre, apellido=apellido, dni=dni, email=email, direccion=direccion, tel1=telefono1, tel2=telefono2, username=username, password=password) 
    res.save()
    return render_to_response("registrar_jugador.html",{"res": res})

def eliminar_jugador(request):
  query = request.GET.get('q', '')
  if query:
      qset = (Q(nombre__icontains=query) |
      Q(apellido__icontains=query) |
      Q(dni__contains=query))
      results = jugadores.objects.filter(qset).distinct()
      res=results.delete()
  else:
	res = []
  return render_to_response("search_player.html",{"res": res,"query": query})

