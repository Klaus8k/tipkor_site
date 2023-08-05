import datetime
from loguru import logger

from django.db import models


class Clients(models.Model):
    name = models.CharField(max_length=50, blank=True, default='anon')
    email = models.EmailField(blank=True)
    tel = models.CharField(max_length=15, blank=True)
    
    def __str__(self):
        return f'{self.name} - e-mail:{self.email} tel: {self.tel}'
    
    @staticmethod
    def get_client_obj(**data: dict):
        try:
            client_obj = Clients.objects.get(**data)
            return client_obj
        except: 
            new_client = Clients(**data)
            new_client.save()
            return new_client
        

class Orders(models.Model):
    client = models.ForeignKey(Clients, on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now=True)
    product = models.JSONField(blank=True)
    comment = models.TextField(max_length=200, blank=True)
    delivery = models.CharField(max_length=100, blank=True, default='no')
    ready_date = models.DateField(blank=True)
    pay_info = models.BooleanField(blank=True, default=False)
    file = models.FileField(upload_to='orders/', blank=True)
    
    def __str__(self):
        return f'client: {self.client}, prof: {self.product} date: {self.create_date}'
       

def date_to_ready(type_production):
    """Расчитывает дату готовности. Если после 15-00 и до 9-00 то + 1 день.
    Если на выходные попадает то до близжайшего понедельника переносится дата
    work_time - Времы работы над заказом
    Returns:
        date: Дата готовности заказа
    """
    
    if type_production in ['booklet', 'table']:
        work_time = 2
    else: work_time = 1


    time_create = datetime.datetime.now()
    # print('часов -', time_create.hour)
    if time_create.hour >= 15 or time_create.hour <= 9 or time_create.weekday() >= 5:
        start_time = time_create + datetime.timedelta(days=1)
        if start_time.weekday() >= 5:
            while start_time.weekday() != 0:
                start_time += datetime.timedelta(days=1)
                
    logger.debug(start_time)
    time_ready = start_time + datetime.timedelta(days=work_time)
    if time_ready.weekday() >= 5: # если на субботу или воскресенье попадает - переносится на понедельник готовность.
        while time_ready.weekday() != 0:
            time_ready += datetime.timedelta(days=work_time)
    return time_ready


# если сейчас больше 15 и меньше 9
#     старт должен быть на следующий день в 9
#         если день выходной
#             старт 9 утра в понедельник
            
# готовность = старт + рабочее время
# если готовность на входной
#     слудующий за выходным день.