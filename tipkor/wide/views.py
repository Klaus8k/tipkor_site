from django import forms
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render, reverse
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormMixin
from loguru import logger
from order.models import Clients, Orders, date_to_ready
from order.sender import send_email

from .forms import Banner_Form, Confirm_form, Sticker_Form, Table_Form
from .models import Wide


class WideMeta(TemplateView, FormMixin):
    form_class = None
    template_name = ''
    model_class = None
    type_production = None
    
    def post(self, *args, **kwargs):
        form = self.form_class(self.request.POST)
        if form.is_bound:
            type_production = self.template_name.split('.')[0]
            self.data_form = self.get_form_dict()
            self.data_form.update({'type_production': type_production})
            self.result = Wide.get_wide_object(self.data_form)
            kwargs.update({'result': self.result})
            kwargs.update({'ready_date': date_to_ready(type_production=type_production)})
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
        # form_dict.update({'type_production':self.type_production})
        del form_dict['csrfmiddlewaretoken']
        del form_dict['calc_form']
        return form_dict
        
    class Meta:
        abstract = True


class BannerView(WideMeta):
    form_class = Banner_Form
    template_name = 'banner.html'
    # type_production = 'banner'

class StickerView(WideMeta):
    form_class = Sticker_Form
    template_name = 'sticker.html'
    # type_production = 'sticker'
    
    
class TableView(WideMeta):
    form_class = Table_Form
    template_name = 'table.html'
    # type_production = 'table'
    
    
class ConfirmView(DetailView, FormMixin):
    model = Wide
    template_name = 'wide/confirm.html'
    form_class = Confirm_form
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        logger.debug(context)
        context['order'] =  self.get_object()
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
        
        order = Orders.objects.create(client=client,
                                      product=product,
                                      ready_date=date_to_ready(confirm_dict['type_production']),
                                      comment=comment,
                                      file=file)
        
        if email:
            send_email(email, order=order)
        return HttpResponseRedirect(reverse('wide:success', kwargs={'pk': order.id}) + '#a_success')
    
    
    def get_order_type(self):
        self.order_type = self.request.META.get('HTTP_REFERER').split('/')[-2]
        if self.order_type == 'banner':
            return 'Баннер'
        elif self.order_type == 'sticker':
            return 'Наклейка'
        elif self.order_type == 'table':
            return 'Табличка'
        else: return 'Изделие не определено'
        
    
class SuccessView(DetailView):
    model = Orders
    template_name = 'wide/success.html'
    context_object_name = 'order'

    

        
    
    