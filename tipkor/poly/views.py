
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, reverse
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormMixin


from order.models import Orders, Clients
from .forms import Card_Form, Confirm_form
from .models import Poly

# Делаем 3 отдельными классами пока

class PolyMeta(TemplateView, FormMixin):
    form_class = None
    template_name = ''
    model_class = None

    def post(self, *args, **kwargs):
        self.data_form = self.get_form_dict()
        self.result = Poly.objects.get(**self.data_form) # it get obj from model poly
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
        del form_dict['csrfmiddlewaretoken']
        del form_dict['calc_form']
        return form_dict
        
    class Meta:
        abstract = True


class CardView(PolyMeta):
    form_class = Card_Form
    template_name = 'card.html'


# class LeafletView(PolyMeta):
#     type_production = 'leaflet'
#     form_class = Leaflet_Form
#     template_name = 'leaflet.html'
#     model_class = Leaflets_Model
    
    
# class BookletView(TemplateView):

#     # model = Cards
#     # context_object_name = 'booklet'
#     template_name = 'booklet.html'
    
    
# Вьюха для подтверждения заказа, контактов и макета
class ConfirmView(DetailView, FormMixin):
    model = Poly
    template_name = 'confirm.html'
    context_object_name = 'order'
    form_class = Confirm_form
    
    def post(self, *args, **kwargs):
        kwargs['pk'] = 3
        
        return HttpResponseRedirect(reverse('poly:success', args=[3]))
    
    
        
    
class SuccessView(DetailView):
    model = Orders
    template_name = 'success.html'
    context_object_name = 'order'

    

        
    
    