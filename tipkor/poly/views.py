
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, reverse
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormMixin
from order.models import Clients, Orders, date_to_ready
from order.sender import send_email

from .forms import Card_Form, Confirm_form
from .models import Poly

# Делаем 3 отдельными классами пока

class PolyMeta(TemplateView, FormMixin):
    form_class = None
    template_name = ''
    model_class = None
    

    def post(self, *args, **kwargs):
        self.data_form = self.get_form_dict()
        self.result = Poly.objects.get(**self.data_form) #TODO get_or_404 
        kwargs.update({'result': self.result})
        kwargs.update({'ready_date': date_to_ready()})
        return self.get(*args, **kwargs)
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.get_form().is_bound:
            context.update({'calc_form': self.form_class(self.data_form)})       
            print(self.data_form)     
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
    # default_calc = {'paper': '300', 'format_p': '1', 'duplex': 'True', 'pressrun': '1000'}


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
        name = self.request.POST.dict()['name'].lower()
        
        email = self.request.POST.dict()['email'].lower()
        # test email sender = 'klaus8@mail.ru'
        # email = 'klaus8@mail.ru'
        
        tel = self.request.POST.dict()['tel']
        client = Clients.objects.get_or_create(name=name,email=email,tel=tel)
        product = self.get_object().json_combine()
        order = Orders.objects.create(client=client[0], product=product, ready_date=date_to_ready())
        
        send_email(email, order=order)
        
        return HttpResponseRedirect(reverse('poly:success', args=[order.id]))
    
    
class SuccessView(DetailView):
    model = Orders
    template_name = 'success.html'
    context_object_name = 'order'

    

        
    
    