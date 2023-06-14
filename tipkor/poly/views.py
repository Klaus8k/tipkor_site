from typing import Any, Dict

from django.http import HttpRequest, HttpResponse
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormMixin

from .forms import Card_Form, Leaflet_Form
from .models import Card_Model, Leaflets_Model

# Делаем 3 отдельными классами пока

class PolyMeta(TemplateView, FormMixin):
    type_production = None
    form_class = None
    template_name = ''
    model_class = None


    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        """Если ПОСТ запрос, чистит данные из формы, добавляет в форму данные
        Args:
            request (HttpRequest): 
        Returns:
            HttpResponse: Передается в ГЕТ объекта, для расчета и отображения шаблона
        """
        self.data_form = self.get_form_data()
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class(self.data_form)
        return self.get(request, *args, **kwargs)

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        """Если форма привязана - то расчет и добавление в контекст kwargs
        Args:
            request (HttpRequest): Свежий или из пост запроса
        Returns:
            HttpResponse: в супер класс обогащенный контекст для отображения в шаблоне
        """
        if self.get_form().is_bound:
            result = self.model_class.get_result(**self.data_form)
            kwargs.update({'result': result})
        return super().get(request, *args, **kwargs)
    
    def get_form_data(self) -> Dict:
        """переводит данные из POST в словать
        добавляет тип продукции и убирает токен
        Returns:
            Dict: словарь параметров из формы с типом продукции
        """
        form_data = self.request.POST.copy()
        form_data.update({'type_production': self.type_production})
        del form_data['csrfmiddlewaretoken']
        return form_data.dict()
        
    class Meta:
        abstract = True


class CardView(PolyMeta):
    type_production = 'card'
    form_class = Card_Form
    template_name = 'card.html'
    model_class = Card_Model


class LeafletView(PolyMeta):
    type_production = 'leaflet'
    form_class = Leaflet_Form
    template_name = 'leaflet.html'
    model_class = Leaflets_Model
    

    

class BookletView(TemplateView):

    # model = Cards
    # context_object_name = 'booklet'
    template_name = 'booklet.html'
