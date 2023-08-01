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

# Делаем 3 отдельными классами пока

class StampMeta(TemplateView, FormMixin):
    form_class = None
    template_name = ''
    model_class = None
    

    def post(self, *args, **kwargs):
        self.data_form = self.get_form_dict()
        self.data_form.update({'type_stamp': self.template_name.split('.')[0]})
        logger.debug(self.data_form)
        self.result = Stamp.get_stamp_object(self.data_form)
        kwargs.update({'result': self.result})
        kwargs.update({'ready_date': date_to_ready()})
        return self.get(*args, **kwargs)
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.get_form().is_bound:
            context.update({'calc_form': self.form_class(self.data_form), 'form': Confirm_form})            
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


class CstampView(StampMeta):
    form_class = C_stamp_Form
    template_name = 'c_stamp.html'
    
class RstampView(StampMeta):
    form_class = R_stamp_Form
    template_name = 'R_stamp.html'
    



class ConfirmView(DetailView, FormMixin):
    model = Stamp
    template_name = 'stamp/confirm.html'
    form_class = Confirm_form
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order'] =  self.get_object() 
        context['ready_date'] =  date_to_ready()
        context['type_production'] = self.get_order_type()
        
        return context
    
    def post(self, *args, **kwargs):
        logger.debug(self.request.FILES)
        name = self.request.POST.dict()['name'].lower()
        email = self.request.POST.dict()['email'].lower()
        comment = self.request.POST.dict()['comment'].lower()
        # file = self.request.POST.dict()['file'].lower()
        # delivery = self.request.POST.dict()['delivery'].lower()
        tel = self.request.POST.dict()['tel']
        client = Clients.objects.get_or_create(name=name,email=email,tel=tel)
        product = self.get_object().json_combine()
        product['type_production'] = self.get_order_type()
        order = Orders.objects.create(client=client[0],
                                      product=product,
                                      ready_date=date_to_ready(),
                                      comment=comment,)
                                    #   file=file)
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

    

        
    
    