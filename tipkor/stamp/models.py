from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from loguru import logger

# Create your models here.
class Snap_type(models.Model):
    snap_type = models.CharField(max_length=20)
    
    def __str__(self):
        return self.snap_type

class Stamp_type(models.Model):
    type_stamp = models.CharField(choices=[('c_stamp', 'печать'),('r_stamp', 'штамп')], max_length=30)
    
    def __str__(self):
        return self.type_stamp
    
class Snap_item(models.Model):
    title = models.CharField(max_length=30)
    type_stamp = models.ForeignKey(Stamp_type, on_delete=models.DO_NOTHING)
    snap_type = models.ForeignKey(Snap_type, on_delete=models.DO_NOTHING)
    snap_img = models.ImageField()
    price = models.IntegerField()
    
    def __str__(self):
        return self.title
    
class Stamp(models.Model):
    type_stamp = models.ForeignKey(Stamp_type, on_delete=models.DO_NOTHING)
    express = models.BooleanField(default=False)
    file = models.FileField(upload_to='orders', blank=True)
    comment = models.TextField(blank=True, max_length=100)
    snap = models.ForeignKey(Snap_item, on_delete=models.DO_NOTHING)
    count = models.IntegerField(default=1)
    cost = models.IntegerField()
    
    def __str__(self):
        return f'{self.type_stamp.type_stamp} {self.snap.title} {self.count}'
    
    @staticmethod
    def get_stamp_object(form_data):
        file = form_data['file']
        comment = form_data['comment']
        snap = Snap_item.objects.get(id=form_data['snap'])
        count = form_data['count']
        type_stamp = Stamp_type.objects.get(type_stamp=form_data['type_stamp'])
        try:
            result = Stamp.objects.get(type_stamp=type_stamp, snap=snap, count=count)
            return result
        except ObjectDoesNotExist:

            cost = Snap_item.objects.get(id=form_data['snap']).price + 500
            form_data.update({'cost': cost, 'type_stamp': type_stamp})
            form_data['snap'] = snap
            new_stamp_object = Stamp(**form_data)
            new_stamp_object.save()
            return new_stamp_object