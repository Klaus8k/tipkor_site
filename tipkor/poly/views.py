from typing import Any, Dict

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, TemplateView, View
from django.views.generic.edit import FormMixin

from .forms import Card_Form
from .models import Card_Model, Leaflets_Model


# Делаем 3 отдельными классами пока
class CardView(ListView, FormMixin):
    model = Card_Model
    context_object_name = 'card'
    template_name = 'card.html'
    # form_class = Card_Form
    

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        a = Card_Form()
        context['card_form'] = a
        return context

class LeafletView(ListView):
    model = Leaflets_Model
    context_object_name = 'leaflet'
    template_name = 'leaflet.html'

class BookletView(TemplateView):

    # model = Cards
    # context_object_name = 'booklet'
    template_name = 'booklet.html'
