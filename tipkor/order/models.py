import datetime

from django.db import models


class Clients(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    tel = models.CharField(max_length=15)
    
    def __str__(self):
        return f'{self.name} - e-mail:{self.email} tel: {self.tel}'

class Orders(models.Model):
    client = models.ForeignKey(Clients, on_delete=models.DO_NOTHING)
    create_date = models.DateTimeField(auto_now=True)
    product = models.JSONField(null=True, blank=True)
    comment = models.TextField(max_length=200, blank=True, null=True)
    delivery = models.CharField(max_length=100, blank=True, default='no')
    ready_date = models.DateField(null=True, blank=True)
    pay_info = models.BooleanField(null=True, blank=True)
    file = models.FileField(upload_to='orders/', null=True, blank=True)
    
    def __str__(self):
        return f'{self.client} - {self.create_date}'
       

def date_to_ready():
    """Расчитывает дату готовности. Если после 15-00 и до 9-00 то + 1 день.
    Если на выходные попадает то до близжайшего понедельника переносится дата
    work_time - Времы работы над заказом
    Returns:
        date: Дата готовности заказа
    """
    work_time = 1
    time_create = datetime.datetime.now()
    # print('часов -', time_create.hour)
    if time_create.hour >= 15 or time_create.hour <= 9: # если заказ после 15-00 то +1 день на работу
        work_time += 1
    time_ready = time_create + datetime.timedelta(days=work_time)
    if time_ready.weekday() >= 5: # если на субботу или воскресенье попадает - переносится на понедельник готовность.
        while time_ready.weekday() != 0:
            time_ready += datetime.timedelta(days=1)
    return time_ready