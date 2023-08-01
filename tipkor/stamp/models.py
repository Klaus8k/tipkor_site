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
    type_stamp = models.ForeignKey(Stamp_type, on_delete=models.DO_NOTHING)
    snap_type = models.ForeignKey(Snap_type, on_delete=models.DO_NOTHING)
    snap_img = models.ImageField(blank=True, null=True,)
    price = models.IntegerField()
    
    def __str__(self):
        return self.title
    
class Stamp(models.Model):
    type_stamp = models.ForeignKey(Stamp_type, on_delete=models.DO_NOTHING)
    express = models.BooleanField(default=False)
    # file = models.FileField(upload_to='orders', null=True, blank=True)
    comment = models.CharField(blank=True, max_length=20)
    snap= models.ForeignKey(Snap_item, blank=True, null=True, on_delete=models.DO_NOTHING)
    count = models.IntegerField(default=1)
    cost = models.IntegerField()
    
    def __str__(self):
        return f'{self.type_stamp.type_stamp} {self.snap.title} {self.count}'
    
    @staticmethod
    def get_stamp_object(form_data):
        # file = form_data['file']       
        express = 'express' in form_data.keys()
        comment = form_data['comment']
        snap = Snap_item.objects.get(id=form_data['snap'])
        count = int(form_data['count'])
        type_stamp = Stamp_type.objects.get(type_stamp=form_data['type_stamp'])
        try:
            result = Stamp.objects.get(type_stamp=type_stamp, snap=snap, count=count, express=express)
            return result
        except ObjectDoesNotExist:            
            if express:
                cost = (Snap_item.objects.get(id=form_data['snap']).price + 1000) * count
            else:       
                cost = (Snap_item.objects.get(id=form_data['snap']).price + 500) * count
            form_data.update({'cost': cost, 'type_stamp': type_stamp, 'express': express})
            form_data['snap'] = snap
            new_stamp_object = Stamp(**form_data)
            new_stamp_object.save()
            return new_stamp_object
        
        
    def json_combine(self):
        json_dict = {'id': self.id,
                     'express': self.express,
                     'comment': self.comment,
                     'snap': self.snap.__str__(),
                     'count': self.count,
                     'cost': self.cost
                     }
        return json_dict 