from typing import Any, Dict

from django.forms import ModelForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls.base import reverse_lazy
from django.views.generic import (CreateView, FormView, ListView, TemplateView,
                                  View)
from django.views.generic.base import ContextMixin, TemplateView
from django.views.generic.edit import FormMixin

from .forms import Card_Form
from .models import Card_Model, Leaflets_Model

# Делаем 3 отдельными классами пока

class PolyMeta(TemplateView, FormMixin):

    form_class = None
    template_name = ''
    success_url = reverse_lazy('')      
    model_class = None


    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        data_from_form = self.get_form_kwargs()['data'].dict()
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class(data_from_form)
        return self.get(HttpRequest, *args, **kwargs)

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        if self.get_form().is_bound:
            self.data_form = self.get_form_kwargs()['data'] # Из реквеста берем данные формы
            self.data_form = self.data_form.dict()
            self.data_form.pop('csrfmiddlewaretoken')
            kwargs.update({'result' : self.model_class.get_cost(**self.data_form)})
        return super().get(request, *args, **kwargs)

    class Meta:
        abstract = True


class CardView(PolyMeta):
    form_class = Card_Form
    template_name = 'card.html'
    success_url = reverse_lazy('poly:card')      
    model_class = Card_Model





class LeafletView(ListView):
    model = Leaflets_Model
    context_object_name = 'leaflet'
    template_name = 'leaflet.html'

class BookletView(TemplateView):

    # model = Cards
    # context_object_name = 'booklet'
    template_name = 'booklet.html'
