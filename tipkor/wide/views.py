from django.shortcuts import render


# Create your views here.

from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, reverse
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormMixin
from order.models import Clients, Orders, date_to_ready
from order.sender import send_email

from .forms import Banner_Form, Sticker_Form, Table_Form, Confirm_form
from .models import Wide

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


class BannerView(PolyMeta):
    form_class = Banner_Form
    template_name = 'banner.html'
    # default_calc = {'paper': '300', 'format_p': '1', 'duplex': 'True', 'pressrun': '1000'}
    
class StickerView(PolyMeta):
    form_class = Sticker_Form
    template_name = 'sticker.html'
    
class TableView(PolyMeta):
    form_class = Table_Form
    template_name = 'table.html'


class ConfirmView(DetailView, FormMixin):
    model = Wide
    template_name = 'confirm.html'
    form_class = Confirm_form
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order'] =  self.get_object() 
        context['ready_date'] =  date_to_ready()
        context['type_production'] = self.get_order_type()
        
        return context
    
    def post(self, *args, **kwargs):
        name = self.request.POST.dict()['name'].lower()
        
        email = self.request.POST.dict()['email'].lower()
        # test email sender = 'klaus8@mail.ru'
        # email = 'klaus8@mail.ru'
        
        tel = self.request.POST.dict()['tel']
        client = Clients.objects.get_or_create(name=name,email=email,tel=tel)
        product = self.get_object().json_combine()
        product['type_production'] = self.get_order_type()
        order = Orders.objects.create(client=client[0], product=product, ready_date=date_to_ready())
        
        send_email(email, order=order)
        
        return HttpResponseRedirect(reverse('wide:success', args=[order.id]))
    
    def get_order_type(self):
        order_type = self.request.path.split('/')[2]
        if order_type == 'banner':
            return 'Баннер'
        elif order_type == 'sticker':
            return 'Наклейка'
        elif order_type == 'table':
            return 'Табличка'
        else: return 'Изделие не определено'
        
    
    
class SuccessView(DetailView):
    model = Orders
    template_name = 'success.html'
    context_object_name = 'order'

    

        
    
    