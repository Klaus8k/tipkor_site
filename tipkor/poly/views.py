
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, reverse
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormMixin
from order.models import Clients, Orders

from .forms import Card_Form, Confirm_form
from .models import Poly, date_to_ready


# Делаем 3 отдельными классами пока

class PolyMeta(TemplateView, FormMixin):
    form_class = None
    template_name = ''
    model_class = None

    def post(self, *args, **kwargs):
        self.data_form = self.get_form_dict()
        self.result = Poly.objects.get(**self.data_form) # it get obj from model poly
        kwargs.update({'result': self.result})
        kwargs.update({'ready_date': date_to_ready()})
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


class ConfirmView(DetailView, FormMixin):
    model = Poly
    template_name = 'confirm.html'
    form_class = Confirm_form
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order'] =  self.get_object() 
        context['ready_date'] =  date_to_ready()
        return context
    
    def post(self, *args, **kwargs):
        name = self.request.POST.dict()['name']
        email = self.request.POST.dict()['email']
        tel = self.request.POST.dict()['tel']
        client = Clients.objects.create(name=name,email=email,tel=tel)
        product = self.get_object().json_combine()
        order = Orders.objects.create(client=client, product=product)
        order_id = order.id
        return HttpResponseRedirect(reverse('poly:success', args=[order_id]))
    
    
class SuccessView(DetailView):
    model = Orders
    template_name = 'success.html'
    context_object_name = 'order'

    

        
    
    