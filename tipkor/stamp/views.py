import datetime

from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, reverse
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormMixin
from loguru import logger
from order.models import Clients, Orders
from order.sender import send_email

from .forms import C_stamp_Form, Confirm_form, R_stamp_Form
from .models import Stamp, stamp_ready_time


class StampMeta(TemplateView, FormMixin):
    form_class = None
    template_name = ''
    model_class = None
        
    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)
        if 'pk' in kwargs.keys(): # Object from calculation
            stamp_obj = Stamp.objects.get(id=kwargs['pk'])
            context.update({'form': self.form_class(instance=stamp_obj)})
            # form with ID calc to success order
            confirm_form = Confirm_form(initial={'id_stamp_obj': kwargs['pk']})
            # If not new stamp, must upload file
            if stamp_obj.new_or_no != 'new':
                confirm_form.fields['file'].required = True
                
            context.update({'confirm_form': confirm_form})
            context.update({'result': Stamp.objects.get(id=kwargs['pk'])})
            context.update({'ready_date': stamp_ready_time(stamp_obj.express)})
        else:
            context.update({'form': self.form_class()})
        return context
    
    def post(self, *args, **kwargs):
        
        self.data_form = self.get_form_dict()
        self.data_form.update({'type_stamp': self.template_name.split('.')[0]})
        self.result = Stamp.get_stamp_object(self.data_form)

        # kwargs.update({'result': self.result})
        # kwargs.update({'ready_date': stamp_ready_time(self.result.express)})
        return HttpResponseRedirect(reverse(f"stamp:{self.data_form['type_stamp']}",
                                            args=[self.result.id]))
        
        
    def get_form_dict(self):
        form_dict = self.request.POST.copy().dict()
        del form_dict['csrfmiddlewaretoken']
        return form_dict


class CstampView(StampMeta):
    form_class = C_stamp_Form
    template_name = 'c_stamp.html'
    
class RstampView(StampMeta):
    form_class = R_stamp_Form
    template_name = 'r_stamp.html'
    

class ConfirmView(DetailView):
    model = Stamp

    def get_context_data(self, **kwargs):
        stamp_obj = self.get_object() 
        context = super().get_context_data(**kwargs)
        context['order'] =  stamp_obj
        context['ready_date'] =  stamp_ready_time(stamp_obj.express)
        return context
    
    def post(self, *args, **kwargs):
        confirm_dict = self.request.POST.dict()
        
        id_stamp = confirm_dict['confirm_form-id_stamp_obj']
        stamp_obj = Stamp.objects.get(id=id_stamp)
        # Get client data from form
        name = confirm_dict['confirm_form-name'].lower()
        email = confirm_dict['confirm_form-email'].lower()
        tel = confirm_dict['confirm_form-tel']
        client = Clients.get_client_obj(name=name,email=email,tel=tel)

        comment = confirm_dict['confirm_form-comment']

        if 'confirm_form-file' in self.request.FILES:
            file = self.request.FILES['confirm_form-file']
        else: file = None
            
        # delivery = self.request.POST.dict()['delivery'].lower()
        
        product = stamp_obj.json_combine()
        product['type_production'] = self.get_order_type()
        order = Orders.objects.create(client=client,
                                      product=product,
                                      ready_date=stamp_ready_time(stamp_obj.express),
                                      comment=comment,
                                      file=file)
                                    #   delivery=delivery)
        if email:
            send_email(email, order=order)
        
        # return HttpResponseRedirect(reverse('stamp:success', args=[order.id] + '#success'))
        return HttpResponseRedirect(reverse('stamp:success', kwargs={'pk': order.id}) + '#a_success')
    
    def get_order_type(self):
        order_type = self.request.META.get('HTTP_REFERER').split('/')[-3]
        if order_type == 'c_stamp':
            return 'Печать'
        elif order_type == 'r_stamp':
            return 'Штамп'
        else: return 'Изделие не определено'
        
    
class SuccessView(DetailView):
    model = Orders
    template_name = 'stamp/success.html'
    context_object_name = 'order'

    

        

    