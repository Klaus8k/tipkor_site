from django.db import models

# Create your models here.
# class Snap(models.Model):
    
#     form = models.CharField(max_length=30)
#     x = models.IntegerField()
#     y = models.IntegerField()
#     price = models.IntegerField()
    
class Stamp(models.Model):
    type_stamp = models.CharField(choices=[
                                    ('c_stamp', 'печать'),
                                    ('r_stamp', 'штампа')],
                                  max_length=50)
    
    express = models.BooleanField()
    file = models.FileField()
    comment = models.TextField(blank=True)
    snap = models.CharField(choices=[('авто','авто'),('обычная','обычная')], max_length=50)
    count = models.IntegerField()
    cost = models.IntegerField()
    