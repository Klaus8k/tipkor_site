from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import ListView


def error_404_view(request, exeption):
    response = render(request, template_name='404.html')
    response.status_code = 404
    return response

def server_error(request):
    return render(request, template_name='404.html')