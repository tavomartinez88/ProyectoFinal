from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse
from django.template import RequestContext
from proyectoFinal.citys.models import City
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf

