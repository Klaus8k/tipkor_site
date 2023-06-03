from typing import Any, Dict

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, TemplateView, View

from .models import Cards, Leaflets


# Делаем 3 отдельными классами пока
class CardView(ListView):
    model = Cards
    context_object_name = 'card'
    template_name = 'card.html'

    # def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
    #     context = super().get_context_data(**kwargs)
    #     context['leaf'] = Leaflets.objects.all()
    #     return context

class LeafletView(ListView):
    model = Leaflets
    context_object_name = 'leaflet'
    template_name = 'leaflet.html'

class BookletView(TemplateView):

    # model = Cards
    # context_object_name = 'booklet'
    template_name = 'booklet.html'
