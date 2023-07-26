import json

from django.core.exceptions import ObjectDoesNotExist, ValidationError
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
    post_obr = models.CharField(choices=POST_OBR, max_length=30)
    cost = models.IntegerField()
    
    def __str__(self):
        return f'{self.wide_size}x{self.heigth_size}_{self.material_print}_{self.post_obr}--{self.cost}'

    @staticmethod
    def get_cost(form_data):
        x = float(form_data['wide_size'])
        y = float(form_data['heigth_size'])
        material = Material.objects.get(id=int(form_data['material_print']))
        
        # get_or_create
        try:
            result = Wide.objects.get(wide_size=x,heigth_size=y, material_print=material)
            return result
        except ObjectDoesNotExist:
            # new_wide_object = Wide.objects.create(wide_size=x,heigth_size=y, material_print=material)
            form_data['material_print'] = Material.objects.get(id=form_data['material_print'])
            cost = x*y*material.cost_per_m
            new_wide_object = Wide(**form_data, cost=cost)
            new_wide_object.save()
            return new_wide_object
        
    def json_combine(self):
        json_dict = {'id': self.id,
                     'material': self.material_print.__str__(),
                     'x': self.wide_size,
                     'y': self.heigth_size,
                     'post_obr': self.post_obr,
                     'cost': self.cost
                     }
        return json_dict



