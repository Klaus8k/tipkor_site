import pprint
from typing import Any, Dict

from django.shortcuts import redirect
from django.http import HttpRequest, HttpResponse
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormMixin

from .forms import Card_Form, Leaflet_Form, Confirm_form
from .models import Card_Model, Leaflets_Model, Order_Model

# Делаем 3 отдельными классами пока

class PolyMeta(TemplateView, FormMixin):
    type_production = None
    form_class = None
    template_name = ''
    model_class = None
    confirm_form = Confirm_form()

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:

        
        
        if self.get_form().is_bound:
            
            self.data_form = self.get_form_data()
            self.result = self.model_class.get_result(**self.data_form)
            kwargs.update({'result': self.result})
            
            if self.confirm_form.is_bound:
                print('11111111111111', self.confirm_form.is_bound)
                SuccessOrderView.post(request, *args, **kwargs)
        
        return self.get(request, *args, **kwargs)
    
    

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:

        if self.get_form().is_bound:
            kwargs.update({'calc_form': self.form_class(self.data_form)})
            kwargs.update({'confirm_form': self.confirm_form})
            
        else:
            kwargs.update({'calc_form': self.form_class()})

            
        
 
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
    
    
    
class SuccessOrderView(TemplateView):
    model_class = Order_Model
    template_name = 'success_order.html'
    
    def post(self, request, *args, **kwargs):
        print('32333333333333333333333333')
        
        return super().get(request, *args, **kwqrgs)
    


        
