from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, reverse
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormMixin
from loguru import logger
from order.models import Clients, Orders, date_to_ready
from order.sender import send_email

from .forms import C_stamp_Form, Confirm_form, R_stamp_Form
from .models import Stamp


class StampMeta(TemplateView, FormMixin):
    form_class = None
    template_name = ''
    model_class = None
        
    def get_context_data(self, **kwargs):
        logger.debug(f'get_request: {kwargs}')
        
        
        context = super().get_context_data(**kwargs)
        if 'pk' in kwargs.keys():
            stamp_obj = Stamp.objects.get(id=kwargs['pk'])
            context.update({'form': self.form_class(instance=stamp_obj)})
            
            confirm_form = Confirm_form(initial={'id_stamp_obj': kwargs['pk']})
            context.update({'confirm_form': confirm_form})
            
            context.update({'result': Stamp.objects.get(id=kwargs['pk'])})
        else:
            context.update({'form': self.form_class()})
        return context
    
    def post(self, *args, **kwargs):
        logger.debug(f'post_request: {self.request.POST}')
        
        self.data_form = self.get_form_dict()
        self.data_form.update({'type_stamp': self.template_name.split('.')[0]})

        self.result = Stamp.get_stamp_object(self.data_form)

        kwargs.update({'result': self.result})
        kwargs.update({'ready_date': date_to_ready()})
        return HttpResponseRedirect(reverse('stamp:c_stamp', args=[self.result.id]))
        
        
    def get_form_dict(self):
        form_dict = self.request.POST.copy().dict()
        del form_dict['csrfmiddlewaretoken']
        return form_dict


class _StampMeta(TemplateView, FormMixin):
    form_class = None
    confirm_form = Confirm_form
    template_name = ''
    model_class = None
    

    def post(self, *args, **kwargs):
        self.data_form = self.get_form_dict()
        self.data_form.update({'type_stamp': self.template_name.split('.')[0]})
        self.result = Stamp.get_stamp_object(self.data_form)
        kwargs.update({'result': self.result})
        kwargs.update({'ready_date': date_to_ready()})
        
        return self.get(*args, **kwargs)
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.get_form().is_bound:
            context.update({'form': self.form_class(self.data_form), 'confirm_form': self.confirm_form})         
        else:
            context.update({'form': self.form_class()})
        return context
    
    def get_form_dict(self):
        form_dict = self.request.POST.copy().dict()
        del form_dict['csrfmiddlewaretoken']
        return form_dict
        
    class Meta:
        abstract = True


class CstampView(StampMeta):
    form_class = C_stamp_Form
    template_name = 'c_stamp.html'
    

class ConfirmView(DetailView):
    model = Stamp
    template_name = 'stamp/confirm.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order'] =  self.get_object() 
        context['ready_date'] =  date_to_ready()
        context['type_production'] = self.get_order_type()
        
        
        return context
    
    def post(self, *args, **kwargs):
        logger.debug(f'FILES - {self.request.FILES}')
        name = self.request.POST.dict()['confirm_form-name'].lower()
        email = self.request.POST.dict()['confirm_form-email'].lower()
        comment = self.request.POST.dict()['confirm_form-comment'].lower()
        file = self.request.FILES['confirm_form-file']
        # delivery = self.request.POST.dict()['delivery'].lower()
        tel = self.request.POST.dict()['confirm_form-tel']
        
        stamp_obj_pk = self.request.POST.dict()['confirm_form-id_stamp_obj']
        client = Clients.objects.get_or_create(name=name,email=email,tel=tel)
        
        product = Stamp.objects.get(id=stamp_obj_pk).json_combine()
        product['type_production'] = self.get_order_type()
        
        order = Orders.objects.create(client=client[0],
                                      product=product,
                                      ready_date=date_to_ready(),
                                      comment=comment,
                                      file=file)
                                    #   delivery=delivery)
        
        send_email(email, order=order)
        
        return HttpResponseRedirect(reverse('stamp:success', args=[order.id]))
    
    def get_order_type(self):
        order_type = self.request.path.split('/')[2]
        if order_type == 'c_stamp':
            return 'Печать'
        elif order_type == 'r_stamp':
            return 'Штамп'
        else: return 'Изделие не определено'
        
    
class SuccessView(DetailView):
    model = Orders
    template_name = 'success.html'
    context_object_name = 'order'

    

        
    
    