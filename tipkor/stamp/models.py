from django.db import models


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
    
class Stamp(models.Model):
    type_stamp = models.ForeignKey(Stamp_type, on_delete=models.DO_NOTHING)
    express = models.BooleanField()
    file = models.FileField()
    comment = models.TextField(blank=True, max_length=100)
    snap = models.ForeignKey(Snap_item, on_delete=models.DO_NOTHING)
    count = models.IntegerField()
    cost = models.IntegerField()
    
    