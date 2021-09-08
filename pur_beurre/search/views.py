from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader 

def index(request):
    template = loader.get_template('search/index.html')
    return HttpResponse(template.render(request=request))

def result(request):
    template = loader.get_template('search/result.html')
    return HttpResponse(template.render(request=request))

def aliment(request):
    template = loader.get_template('search/aliment.html')
    return HttpResponse(template.render(request=request))

def compte(request):
    template = loader.get_template('search/compte.html')
    return HttpResponse(template.render(request=request))
