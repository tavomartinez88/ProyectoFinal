from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse

from django.template import RequestContext
from complejos.models import Complejo
from django.db.models import Q
from forms import ComplejoForm
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
def search_form(request):
  query = request.GET.get('q', '')
  if query:
	qset = (Q(nombre__icontains=query))
	results = Complejo.objects.filter(qset).distinct()

  else:
	results = []
  return render_to_response("search_form.html",{"results": results,"query": query})


def crear_form(request):
    nombre = request.GET.get('nombre', '')
    direccion = request.GET.get('direccion', '')
    telefono = request.GET.get('telefono', '')
    nombreTitular = request.GET.get('nombreTitular', '')
    res = Complejo(nombre=nombre, direccion=direccion, telefono=telefono, nombreTitular=nombreTitular)
    res.save()
    return render_to_response("crear_form.html",{"res": res})

def eliminar_form(request):
  query = request.GET.get('q', '')
  if query:
	qset = (Q(nombre__icontains=query))
	results = Complejo.objects.filter(qset).distinct()
	res=results.delete()

  else:
	res = []
  return render_to_response("search_form.html",{"res": res,"query": query})
