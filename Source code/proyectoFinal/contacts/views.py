#encoding:utf-8
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from forms import FormularioContacto
from proyectoFinal.publicities.models import Publicity

def contactomail(request):
    try:
      publish_one = Publicity.objects.all().order_by('?').first()
    except Exception:
      publish_one = False
    try:
      publish_second = Publicity.objects.all().exclude(id=publish_one.id).order_by('?').last()
    except Exception:
      publish_second = False
    if request.method == 'POST':
    	formulario = FormularioContacto(request.POST)
        if not formulario.is_valid():
            message = 0
            return render_to_response('contacts/send_mail.html',{'publish_one':publish_one,'publish_second':publish_second,'formulario':formulario,'message': message}, context_instance=RequestContext(request))
        else:
            try:
                asunto = formulario.cleaned_data['Asunto']
                nombre = formulario.cleaned_data['Nombre']
                email = formulario.cleaned_data['Email']
                mensaje = "Has recibido un mensaje de "+nombre+"\nremitente : "+email+"\nMensaje : "+formulario.cleaned_data['Mensaje']
                send_mail(asunto, mensaje, email,['service.minutogol@gmail.com'],fail_silently=False)
                message = 1
            except Exception:
                message = 0
            formulario = FormularioContacto()
            return render_to_response('contacts/send_mail.html',{'publish_one':publish_one,'publish_second':publish_second,'formulario':formulario,'message': message}, context_instance=RequestContext(request))
    else:
    	formulario = FormularioContacto()
    return render_to_response('contacts/send_mail.html',{'publish_one':publish_one,'publish_second':publish_second,'formulario':formulario}, context_instance=RequestContext(request))
    
