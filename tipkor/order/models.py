import datetime

from django.db import models
from loguru import logger


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
    client = models.ForeignKey(Clients, on_delete=models.CASCADE, related_name='client_orders')
    create_date = models.DateTimeField(auto_now=True)
    product = models.JSONField(blank=True)
    comment = models.TextField(max_length=200, blank=True)
    delivery = models.CharField(max_length=100, blank=True, default='no')
    ready_date = models.DateTimeField(blank=True)
    pay_info = models.BooleanField(blank=True, default=False)
    file = models.FileField(upload_to='orders/', blank=True)
    
    def __str__(self):
        return f'client: {self.client}, prof: {self.product} date: {self.create_date}'
       

def date_to_ready(type_production):

    if type_production in ['booklet', 'table']:
        work_time = 2
    else: work_time = 1


    time_create = datetime.datetime.now()
    if time_create.hour >= 15 or time_create.hour <= 9 or time_create.weekday() >= 5:
        start_time = time_create.replace(hour=10)
        start_time = time_create + datetime.timedelta(days=1)
        if start_time.weekday() >= 5:
            while start_time.weekday() in [5,6]:
                start_time += datetime.timedelta(days=1)
    else:
        start_time = datetime.datetime.now()
                
    time_ready = start_time + datetime.timedelta(days=work_time)
    
    if time_ready.weekday() >= 5: # Перенос готовности на понедельник, если выпадает на выходные
        while time_ready.weekday() in [5,6]:
            time_ready += datetime.timedelta(days=1)
    return time_ready
