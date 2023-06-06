from typing import Any, Dict

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import FormView, ListView, TemplateView, View
from django.views.generic.edit import FormMixin
from django.views.generic.base import TemplateView

from .forms import Card_Form
from .models import Card_Model, Leaflets_Model


# Делаем 3 отдельными классами пока
class CardView(TemplateView, FormMixin):
    model = Card_Model
    context_object_name = 'card'
    template_name = 'card.html'
    form_class = Card_Form
    success_url = '/poly/card'

    def form_valid(self, form) -> HttpResponse:
        self.extra_content = {'result': 10} #Нужно отображение результата и заполненной ранее формы, как обогатить контекст заполненной формой?
        self.get_context_data()
        return super().form_valid(form)


    






class LeafletView(ListView):
    model = Leaflets_Model
    context_object_name = 'leaflet'
    template_name = 'leaflet.html'

class BookletView(TemplateView):

    # model = Cards
    # context_object_name = 'booklet'
    template_name = 'booklet.html'
