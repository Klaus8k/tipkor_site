from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, reverse
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormMixin
from loguru import logger
from order.models import Clients, Orders, date_to_ready
from order.sender import send_email

from .forms import Booklet_Form, Card_Form, Confirm_form, Leaflet_Form
from .models import Poly, multiply_cost

# Делаем 3 отдельными классами пока

class PolyMeta(TemplateView, FormMixin):
    form_class = None
    template_name = ''
    model_class = None
    

    def post(self, *args, **kwargs):
        self.data_form = self.get_form_dict()
        self.result = Poly.get_poly_object(self.data_form) #TODO get_or_404 
        kwargs.update({'result': self.result})
        kwargs.update({'ready_date': date_to_ready(self.template_name.split('.')[0])})
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
    

class LeafletView(PolyMeta):
    form_class = Leaflet_Form
    template_name = 'leaflet.html'
    
class BookletView(PolyMeta):
    form_class = Booklet_Form
    template_name = 'booklet.html'


class ConfirmView(DetailView, FormMixin):
    model = Poly
    template_name = 'poly/confirm.html'
    form_class = Confirm_form
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order'] =  self.get_object()
        context['cost'] = multiply_cost(cost=context['object'].cost, pressrun=context['object'].pressrun)
        type_production =  self.get_order_type()
        context['form'] = self.form_class(initial={'type_production': type_production})
        context['ready_date'] =  date_to_ready(type_production=self.order_type)
        context['type_production'] = type_production
        
        return context
    
    def post(self, *args, **kwargs):

        confirm_dict = self.request.POST.dict()
        
        name = confirm_dict['name'].lower()
        email = confirm_dict['email'].lower()
        tel = confirm_dict['tel']
        client = Clients.get_client_obj(name=name,email=email,tel=tel)
        
        comment = confirm_dict['comment']
        if 'file' in self.request.FILES:
            file = self.request.FILES['file']
        else: file = None
        # delivery = self.request.POST.dict()['delivery'].lower()
            
        product = self.get_object().json_combine()
        product['type_production'] = confirm_dict['type_production']
        product['cost'] = multiply_cost(cost=product['cost'], pressrun=product['pressrun'])

        order = Orders.objects.create(client=client,
                                      product=product,
                                      ready_date=date_to_ready(confirm_dict['type_production']),
                                      comment=comment,
                                      file=file)
        
        if email:
            send_email(email, order=order)
        
        return HttpResponseRedirect(reverse('poly:success', kwargs={'pk': order.id}) + '#a_success')
    
    def get_order_type(self):
        self.order_type = self.request.META.get('HTTP_REFERER').split('/')[-2]
        if self.order_type == 'card':
            return 'Визитки'
        elif self.order_type == 'leaflet':
            return 'Листовки'
        elif self.order_type == 'booklet':
            return 'Буклеты'
        else: return 'Изделие не определено'
        
    
class SuccessView(DetailView):
    model = Orders
    template_name = 'poly/success.html'
    context_object_name = 'order'

    

        
    
    