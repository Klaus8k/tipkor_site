from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import ListView


def error_404_view(request, exeption):
    return render(request, template_name='404.html')

def server_error(request):
    return render(request, template_name='404.html')