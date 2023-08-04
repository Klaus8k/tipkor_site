from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from loguru import logger


# Create your models here.
class Snap_type(models.Model):
    title_stap_type = models.CharField(max_length=30, blank=True)
    snap_type = models.CharField(max_length=20, blank=True)
    
    def __str__(self):
        return self.title_stap_type

class Stamp_type(models.Model):
    type_stamp = models.CharField(choices=[('c_stamp', 'печать'),('r_stamp', 'штамп')], max_length=30)
    
    def __str__(self):
        return self.type_stamp
    
class Snap_item(models.Model):
    title = models.CharField(max_length=30)
    type_stamp = models.ForeignKey(Stamp_type, on_delete=models.CASCADE)
    snap_type = models.ForeignKey(Snap_type, on_delete=models.CASCADE)
    snap_img = models.ImageField(blank=True)
    price = models.IntegerField()
    
    def __str__(self):
        return self.title
    
class Stamp(models.Model):
    NEW_CHOICE = (('new', 'Новая'),
                  ('repeat', 'По оттиску'))
    EXPRESS_CHOICE = ((True, 'Срочно'),
                      (False, 'Стандарт'))
    
    
    type_stamp = models.ForeignKey(Stamp_type, on_delete=models.CASCADE)
    new_or_no = models.CharField(choices=NEW_CHOICE, default='new', max_length=20)
    express = models.BooleanField(choices=EXPRESS_CHOICE, default=False)
    snap= models.ForeignKey(Snap_item, blank=True, null=True, on_delete=models.CASCADE)
    count = models.IntegerField(default=1)
    cost = models.IntegerField()
    
    def __str__(self):
        return f'{self.type_stamp.type_stamp} {self.snap.title} {self.count} {self.new_or_no}'
    
    @staticmethod
    def get_stamp_object(form_data):
        express = 'form-express' in form_data.keys()
        new_or_no = form_data['form-new_or_no']
        snap = Snap_item.objects.get(id=form_data['form-snap'])
        count = int(form_data['form-count'])
        type_stamp = Stamp_type.objects.get(type_stamp=form_data['type_stamp'])
        try:
            result = Stamp.objects.get(type_stamp=type_stamp,  new_or_no=new_or_no, snap=snap, count=count, express=express)
            return result
        except ObjectDoesNotExist:            
            if express:
                cost = (Snap_item.objects.get(id=form_data['form-snap']).price + 1000) * count
            else:       
                cost = (Snap_item.objects.get(id=form_data['form-snap']).price + 500) * count
            form_data.update({'cost': cost, 'type_stamp': type_stamp, 'express': express})
            form_data['snap'] = snap
            new_stamp_object = Stamp(type_stamp=type_stamp,
                                     new_or_no=new_or_no,
                                     express=express,
                                     snap=snap,
                                     count=count,
                                     cost=cost                                     
                                     )
            new_stamp_object.save()
            return new_stamp_object
        
        
    def json_combine(self):
        json_dict = {'id': self.id,
                     'new_or_no': self.new_or_no,
                     'express': self.express,
                     'snap': self.snap.__str__(),
                     'count': self.count,
                     'cost': self.cost
                     }
        return json_dict 