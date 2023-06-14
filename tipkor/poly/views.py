from typing import Any, Dict

from django.http import HttpRequest, HttpResponse
from django.urls.base import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormMixin

from .forms import Card_Form, Leaflet_Form
from .models import Card_Model, Leaflets_Model

# Делаем 3 отдельными классами пока

class PolyMeta(TemplateView, FormMixin):
    type_production = None
    form_class = None
    template_name = ''
    success_url = reverse_lazy('')      
    model_class = None
    del_keys = ['csrfmiddlewaretoken']


    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        data_from_form = self.get_form_kwargs()['data'].dict() # TODO - вынести в метод извлечение данных из формы
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class(data_from_form)
        return self.get(HttpRequest, *args, **kwargs)

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        if self.get_form().is_bound:
            self.data_form = self.get_form_kwargs()['data'].dict() # TODO - вынести в метод извлечение данных из формы

            self.data_form['type_production': self.type_production]
            
            del self.data_form['csrfmiddlewaretoken']
            
            # TODO try for 'no matches result'
            result = {'result' : self.model_class.get_result(**self.data_form)} # TODO - приличный словарь для результата сделать. Что бы в шаблонах норм расставить
            print(result['result'].cost)
            kwargs.update(result)
        return super().get(request, *args, **kwargs)

    class Meta:
        abstract = True


class CardView(PolyMeta):
    type_production = 'card'
    form_class = Card_Form
    template_name = 'card.html'
    success_url = reverse_lazy('poly:card')      
    model_class = Card_Model
    del_keys = ['csrfmiddlewaretoken']


class LeafletView(PolyMeta):
    type_production = 'leaflet'
    form_class = Leaflet_Form
    template_name = 'leaflet.html'
    success_url = 'poly:leaflet'
    model_class = Leaflets_Model
    del_keys = ['csrfmiddlewaretoken']
    

    

class BookletView(TemplateView):

    # model = Cards
    # context_object_name = 'booklet'
    template_name = 'booklet.html'
