from typing import Any, Dict

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import ListView

from .models import Cards, Leaflets


class PolyView(ListView):
    model = Cards
    context_object_name = 'cards'
    template_name = 'poly.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['leaf'] = Leaflets.objects.all()
        return context