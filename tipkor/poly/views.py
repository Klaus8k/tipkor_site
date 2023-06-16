
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormMixin
from django.views.generic.detail import DetailView

from .forms import Card_Form, Confirm_form, Leaflet_Form
from .models import Card_Model, Leaflets_Model, Order_Model

# Делаем 3 отдельными классами пока

class PolyMeta(TemplateView, FormMixin):
    type_production = None
    form_class = None
    template_name = ''
    model_class = None

    def post(self, *args, **kwargs):
        self.data_form = self.get_form_dict()
        self.result = self.model_class.get_result(**self.data_form)
        kwargs.update({'result': self.result})   
        return self.get(*args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.get_form().is_bound:
            context.update({'calc_form': self.form_class(self.data_form)})            
        else:
            context.update({'calc_form': self.form_class()})
        return context
    
    
    def get_form_dict(self):
        form_dict = self.request.POST.copy().dict()
        form_dict.update({'type_production': self.type_production})
        del form_dict['csrfmiddlewaretoken']
        del form_dict['calc_form']
        return form_dict
        
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
    
    
# Вьюха для подтверждения заказа, контактов и макета
class ConfirmView(DetailView, FormMixin):
    model = Order_Model
    template_name = 'confirm.html'
    context_object_name = 'order'
    