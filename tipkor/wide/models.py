import json

from django.core.exceptions import ValidationError
from django.db import models
from order.models import Orders

from .constants import POST_OBR


def valid(value):
    if isinstance(value % 1000, int):
        raise ValidationError('должно быть кратно 1000')

class Material(models.Model):
    material = models.CharField(max_length=20)
    cost_per_m = models.IntegerField()
    
    def __str__(self):
        return f'{self.material} - {self.cost_per_m} руб.'
    
    
class Wide(models.Model):
    wide_size = models.FloatField()
    heigth_size = models.FloatField()
    material_print = models.ForeignKey(Material, on_delete=models.DO_NOTHING)
    post_obr = models.CharField(choices=POST_OBR)
    cost = models.IntegerField()
    
    def __str__(self):
        return f'{self.wide_size}x{self.heigth_size}_{self.material_print}_{self.post_obr}--{self.cost}'


    # def json_combine(self):
    #     json_dict = {'id': self.id,
    #                  'format_p': self.format_p.__str__(),
    #                  'paper': self.paper,
    #                  'pressrun': self.pressrun,
    #                  'duplex': self.duplex,
    #                  'post_obr': self.post_obr,
    #                  'cost': self.cost
    #                  }
    #     return json_dict



