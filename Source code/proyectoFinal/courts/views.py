#encoding:utf-8
from django.db.models import Q
from django.shortcuts import render_to_response
from models import Court
from models import Complex
from proyectoFinal.users.models import UserProfile
from proyectoFinal.publicities.models import Publicity
from forms import CourtForm, CourtFormUpdate
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.core.context_processors import csrf # to increase security in the page
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import Http404
from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy


"""
Esta vista se encarga de listar las canchas de un complejo.Solo permitira acceder a esta seccion 
si esta logueado,en caso mostrará las canchas de un complejo determinado de lo contrario no se 
permitirá acceder a dicha sección
"""
def listCourt(request,idcomplex):
  if request.user.is_anonymous():
    return HttpResponseRedirect('/login')
  try:
    usuario = UserProfile.objects.get(user=request.user)
    complejo = Complex.objects.get(id = idcomplex)
  except Exception:
    raise Http404
  if complejo.user_id != usuario.user_id and usuario.userType=='PR':
    message = '''
              Oops!!! ha ocurrido un inconveniente, usted no tiene los permisos necesarios para ver 
              canchas correspondientes a complejos que no son de su propiedad
              '''
    return render_to_response('404.html',{'message':message})  
  if usuario.userType=='CM' or usuario.userType=='PR' :
    courts = Court.objects.filter(complex_id=idcomplex)
    try:
      publish_one = Publicity.objects.all().order_by('?').first()
    except Exception:
      publish_one = False
    try:
      publish_second = Publicity.objects.all().exclude(id=publish_one.id).order_by('?').last()
    except Exception:
      publish_second = False
    
    return render_to_response("courts/listCourts.html",{'publish_one':publish_one,'publish_second':publish_second,"courts": courts, "complejo":complejo}, RequestContext(request, {}))

"""
Esta vista se encarga de actualizar una cancha de un complejo.Solo permitira acceder a esta seccion 
si esta logueado,ser un usuario propietario y ser el propieario de la cancha.
"""
class updateCourt(UpdateView):
  model = Court
  template_name_suffix = '_update_form'
  form_class = CourtFormUpdate

  def get_success_url(self):
    objeto_court_current = self.kwargs['pk']
    id_court = int(x=objeto_court_current)
    try:
      court_current = Court.objects.get(id=id_court)
    except Exception:
      court_current = None
    try:
      complex_current = Complex.objects.get(id = court_current.complex_id)
    except Exception:
      complex_current = None
    return reverse('courts', kwargs={'idcomplex': complex_current.id})

  def get_context_data(self, **kwargs):
      # Call the base implementation first to get a context
      context = super(updateCourt, self).get_context_data(**kwargs)
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

  def get_form_kwargs(self):
  	kwargs = super(updateCourt, self).get_form_kwargs()
  	return kwargs

  def dispatch(self, *args, **kwargs):
    try:
      usuario = UserProfile.objects.get(user=self.request.user)
    except Exception:
      return HttpResponseRedirect('/login')
    if usuario.userType=='CM' or self.request.user.is_anonymous():
      message = '''
                Oops!!! ha ocurrido un inconveniente, no cuentas con los permisos de un usuario propietario
                de canchas.
                '''
      return render_to_response('404.html',{'message':message})
    else:
      return super(updateCourt, self).dispatch(*args, **kwargs)

  def get_object(self, queryset=None):
    #select the court object that we want to update
    cancha = super(updateCourt, self).get_object()
    #select the complex in base of the court
    complejo = Complex.objects.get(id = cancha.complex_id)
    #select the user in base of the complex
    usuario = UserProfile.objects.get(user_id = complejo.user_id)
    if not usuario.user == self.request.user:
      message = '''
                Oops!!! ha ocurrido un inconveniente, no puedes actualizar esta cancha porque no eres su 
                propietario.
                '''
      return render_to_response('404.html',{'message':message})
    return cancha    


"""
Esta vista se encarga de buscar canchas
"""
def search_court(request):
  query = request.GET.get('q', '')
  if query:
    try:
      qset = (Q(complex__name__icontains=query))
      results = Court.objects.filter(qset).distinct()
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
  return render_to_response("courts/searchCourt.html",{'publish_one':publish_one,'publish_second':publish_second,"results": results,"query": query}, RequestContext(request, {}))

"""
Esta vista se encarga de actualizar una cancha de un complejo.Solo permitira acceder a esta seccion 
si esta logueado,debe ser un usuario propietario y ser el propieario de la cancha.
"""
class deleteCourt(DeleteView):
  model = Court
  success_url = '/courts'

  def get_form_kwargs(self):
  	kwargs = super(deleteCourt, self).get_form_kwargs()
  	#kwargs.update({'user': self.request.user})
  	return kwargs

  def get_success_url(self):
    objeto_court_current = self.kwargs['pk']
    id_court = int(x=objeto_court_current)
    court_current = Court.objects.get(id=id_court)
    complex_current = Complex.objects.get(id = court_current.complex_id)
    return reverse('courts', kwargs={'idcomplex': complex_current.id})  


  def dispatch(self, *args, **kwargs):
    try:
      usuario = UserProfile.objetcs.get(user = self.request.user)
    except Exception:
      return HttpResponseRedirect('/login')
    if self.request.user.is_anonymous() or usuario.userType=='CM':
      message = '''
                Oops!!! ha ocurrido un inconveniente, no cuentas con los permisos de un usuario propietario
                de canchas.
                '''
      return render_to_response('404.html',{'message':message})
    return super(deleteCourt, self).dispatch(*args, **kwargs)

  def get_object(self, queryset=None):
    #select the court object that we want to delete
    cancha = super(deleteCourt, self).get_object()
    #select the complex in base of the court
    complejo = Complex.objects.get(id = cancha.complex_id)
    #select the user in base of the complex
    usuario = UserProfile.objects.get(user_id = complejo.user_id)
    if not usuario.user == self.request.user:
      message = '''
                Oops!!! ha ocurrido un inconveniente, no puedes eliminar esta cancha porque no eres su 
                propietario.
                '''
      return render_to_response('404.html',{'message':message})
    return cancha  

  def get_context_data(self, **kwargs):
      # Call the base implementation first to get a context
      context = super(deleteCourt, self).get_context_data(**kwargs)
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
Esta vista se encarga de crear una cancha de un complejo.Solo permitira acceder a esta seccion 
si esta logueado,debe ser un usuario propietario
"""
class CreateCourt(CreateView):
  model = Court
  success_url = '/complexes'
  form_class = CourtForm

  def get_context_data(self, **kwargs):
    context = super(CreateCourt, self).get_context_data(**kwargs)
    try:
      context['publish_one'] = Publicity.objects.all().order_by('?').first()
    except Exception:
      context['publish_one'] = False
    try:
      context['publish_second'] = Publicity.objects.all().exclude(id=context['publish_one'].id).order_by('?').last()
    except Exception:
      context['publish_second'] = False
    return context  

  def get_form_kwargs(self):
    kwargs = super(CreateCourt, self).get_form_kwargs()
    kwargs.update({'user': self.request.user})
    return kwargs

  def dispatch(self, *args, **kwargs):
    if self.request.user.is_anonymous():
      return HttpResponseRedirect('/login')
    else:
      try:
        usuario = UserProfile.objects.get(user=self.request.user)
      except Exception:
        return HttpResponseRedirect('/login')
      if usuario.userType=='PR':
        return super(CreateCourt, self).dispatch(*args,**kwargs)
      else:
        message = '''
                  Oops!!! ha ocurrido un inconveniente, no puedes crear canchas porque no tienes los
                  permisos necesarios.Tambien puedes contactarte para solventar alguna duda.
                  '''
        sendmail = True
        return render_to_response('404.html',{'message':message,'sendmail':sendmail})
    