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
        data_from_form = self.get_form_kwargs()['data'].dict()
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class(data_from_form)
        return self.get(HttpRequest, *args, **kwargs)

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        if self.get_form().is_bound:
            self.data_form = self.get_form_kwargs()['data'] # Из реквеста берем данные формы
            self.data_form = self.data_form.dict()
            self.data_form.update({'type_production': self.type_production})
            for i in self.del_keys:
                self.data_form.pop(i)
            kwargs.update({'result' : self.model_class.get_cost(**self.data_form)})
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
