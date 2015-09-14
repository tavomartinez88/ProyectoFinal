#encoding:utf-8
from django.db.models import Q
from django.shortcuts import render_to_response
from models import Complex , User
from proyectoFinal.users.models import UserProfile
from proyectoFinal.publicities.models import Publicity
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from forms import ComplexForm
from django.http import HttpResponseRedirect
from django.views.generic import ListView, UpdateView, DeleteView
from django.core.context_processors import csrf # to increase security in the page
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import Http404
from django.shortcuts import render

"""
Esta vista se encarga de listar los complejos.SI el usuario no se a logueado o si el usuario logueado
es un ususario con permisos de usuario comun mostrará todos los complejos disponibles.
En caso de que el usuario logueado tiene permisos de usuario propietario solo se mostraran aquellos 
complejos en los cuales es dueño.
"""
class listComplex(ListView):
  template_name = 'complexes/listComplexes.html'
  model = Complex
  context_object_name = 'complexes'
  paginate_by = 6

  def get_queryset(self):
    if self.request.user.is_anonymous():
      return Complex.objects.all()
    else:
      try:
        usuario = UserProfile.objects.get(user=self.request.user)
      except Exception:
        raise Http404
      if usuario.userType=='CM':
        return Complex.objects.all()
      else:
        return Complex.objects.filter(user=self.request.user)

  def get_context_data(self, **kwargs):
      # Call the base implementation first to get a context
      context = super(listComplex, self).get_context_data(**kwargs)
      # Add in the publisher
      try:
        context['publish_one'] = Publicity.objects.all().order_by('?').first()
      except Exception:
        context['publish_one'] = False
      try:
        context['publish_second'] = Publicity.objects.all().exclude(id=context['publish_one'].id).order_by('?').last()
      except Exception:
        context['publish_second'] = False
      return context            


"""
Esta vista se encarga de la busqueda de complejos dinamicamente, se ingresa el nombre del complejo o
una parte del mismo y la vista realizara una busqueda dinamica como lo realiza sql con el patron like
"""
def search_complex(request):
  query = request.GET.get('q', '')
  if query:
    try:
      qset = (Q(name__icontains=query))
      results = Complex.objects.filter(qset).distinct()      
    except Exception:
      raise Http404
  else:
	results = []
  try:
    publish_one = Publicity.objects.all().order_by('?').first()
  except Exception:
    publish_one = False
  try:
    publish_second = Publicity.objects.all().exclude(id=publish_one.id).order_by('?').last()
  except Exception:
    publish_second = False
  return render_to_response("complexes/searchComplex.html",{'publish_one':publish_one,'publish_second':publish_second,"results": results,"query": query}, RequestContext(request, {}))


"""
Esta vista se encarga de la eliminacion de un complejo,la misma toma como requisitos basicos que el usuario
debe estar logueado,debe ser usuario propietario y debe ser el propietario del complejo.
"""
class deleteComplex(DeleteView):
  model = Complex
  success_url = '/complexes'
  def get_form_kwargs(self):
  	kwargs = super(deleteComplex, self).get_form_kwargs()
  	#kwargs.update({'user': self.request.user})
  	return kwargs

  def get_context_data(self, **kwargs):
      # Call the base implementation first to get a context
      context = super(deleteComplex, self).get_context_data(**kwargs)
      # Add in the publisher
      try:
        context['publish_one'] = Publicity.objects.all().order_by('?').first()
      except Exception:
        context['publish_one'] = False
      try:
        context['publish_second'] = Publicity.objects.all().exclude(id=context['publish_one'].id).order_by('?').last()
      except Exception:
        context['publish_second'] = False
      return context        


  def dispatch(self, *args, **kwargs):
    try:
      usuario = UserProfile.objects.get(user = self.request.user)
    except Exception:
      return HttpResponseRedirect('/login')
    if usuario.userType== 'CM' or self.request.user.is_anonymous():
      message = 'Oops!!! ha ocurrido un inconveniente, para poder eliminar el complejo debes ser el propietario del complejo'
      return render_to_response('404.html',{'message':message})
    else:
      return super(deleteComplex, self).dispatch(*args, **kwargs)

  def get_object(self, queryset=None):
    #select the court object that we want to update
    complejo = super(deleteComplex, self).get_object()
    try:
      usuario = UserProfile.objects.get(user_id = complejo.user_id)
    except Exception:
      return HttpResponseRedirect('/login')
    
    if not usuario.user == self.request.user and usuario.userType == 'PR':
      message = 'Oops!!! ha ocurrido un inconveniente, para poder eliminar el complejo debes ser el propietario del complejo'
      return render_to_response('404.html',{'message':message})
    return complejo     
  
"""
Esta vista se encarga de realizar la creación de un complejo,para ello se debera ser un usuario propietario
y ser parte del staff,
"""
def register(request):
  try:
    usuario = UserProfile.objects.get(user=request.user)
  except Exception:
    return HttpResponseRedirect('/login')
  if usuario.userType=='PR' and request.user.is_staff:
    try:
      publish_one = Publicity.objects.all().order_by('?').first()
    except Exception:
      publish_one = False
    try:
      publish_second = Publicity.objects.all().exclude(id=publish_one.id).order_by('?').last()
    except Exception:
      publish_second = False
    if request.POST:
      cform = ComplexForm(request.POST) #create a ComplexForm
      if cform.is_valid() : #if the information in the form its correct
        add=cform.save()
        try:
          add2=Complex.objects.get(id=add.id)
          ident = UserProfile.objects.get(user_id = request.user.id)
        except Exception:
          return HttpResponseRedirect('/login')      
        add2.user_id = ident.user_id
        add2.save()
        return HttpResponseRedirect('/complexes')
    else:
      cform = ComplexForm()
      args = {}
      args.update(csrf(request))
      args['cform'] = cform
      args['publish_one'] = publish_one
      args['publish_second'] = publish_second
      return render_to_response('complexes/register.html', args, RequestContext(request, {}))
  else:
    message = '''Oops!!! ha ocurrido un inconveniente, para poder registrar un complejo necesitas 
                 permisos con los que no cuentas en este momento.Intenta más tarde,si persiste el problema
                 contactanos mencionando tu problema.
              '''
    sendmail = True
    return render_to_response('404.html',{'message':message,'sendmail':sendmail})

"""
Esta vista se encarga de la actualizacion de un complejo,la misma toma como requisitos basicos que el usuario
debe estar logueado,debe ser usuario propietario y debe ser el propietario del complejo.
"""
class updateComplex(UpdateView):
  model = Complex
  form_class = ComplexForm
  template_name_suffix = '_update_complex'
  success_url = '/complexes' #redirect when the edit form is filled

  def get_form_kwargs(self):
  	kwargs = super(updateComplex, self).get_form_kwargs()
  	return kwargs

  def get_context_data(self, **kwargs):
      # Call the base implementation first to get a context
      context = super(updateComplex, self).get_context_data(**kwargs)
      # Add in the publisher
      try:
        context['publish_one'] = Publicity.objects.all().order_by('?').first()
      except Exception:
        context['publish_one'] = False
      try:
        context['publish_second'] = Publicity.objects.all().exclude(id=context['publish_one'].id).order_by('?').last()
      except Exception:
        context['publish_second'] = False
      return context          


  def dispatch(self, *args, **kwargs):
    try:
      usuario = UserProfile.objects.get(user = self.request.user)
    except Exception:
      return HttpResponseRedirect('/login')    
    if usuario.userType== 'CM' or self.request.user.is_anonymous():
      message = '''
                Oops!!! ha ocurrido un error,para poder actualizar este complejo debes ser el propietario
                y contar con los permisos necesarios para poder realizar la operación. Intenta mas tarde y 
                si persiste el inconveniente contactanos.
                '''
      sendmail = True
      return render_to_response('404.html',{'message':message,'sendmail':sendmail})
    else:
      return super(updateComplex, self).dispatch(*args, **kwargs)

  def get_object(self, queryset=None):
    complejo = super(updateComplex, self).get_object()
    try:
      usuario = UserProfile.objects.get(user_id = complejo.user_id)
    except Exception:
      return HttpResponseRedirect('/login')
    if not usuario.user == self.request.user and usuario.userType == 'PR':
      message = '''
                Oops!!! ha ocurrido un error,para poder actualizar este complejo debes ser el propietario
                y contar con los permisos necesarios para poder realizar la operación. Intenta mas tarde y 
                si persiste el inconveniente contactanos.
                '''
      sendmail = True
      return render_to_response('404.html',{'message':message,'sendmail':sendmail})
    return complejo    





