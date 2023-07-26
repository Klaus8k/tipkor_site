import json

from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import models
from order.models import Orders

from .constants import POST_OBR


def valid(value):
    if isinstance(value % 1000, int):
        raise ValidationError('должно быть кратно 1000')

class Material(models.Model):
    material = models.CharField(max_length=30)
    cost_per_m = models.IntegerField()
    
    def __str__(self):
        return f'{self.material} {self.cost_per_m}'
    
class Post_obr(models.Model):
    type_wide_production = models.CharField(max_length=30)
    title_post_obr = models.CharField(max_length=30)
    price = models.IntegerField()
    
    def __str__(self):
        return f'{self.title_post_obr}'
    
    
class Wide(models.Model):
    wide_size = models.FloatField()
    heigth_size = models.FloatField()
    material_print = models.ForeignKey(Material, on_delete=models.DO_NOTHING)
    post_obr = models.ForeignKey(Post_obr, on_delete=models.DO_NOTHING, null=True)
    cost = models.IntegerField()
    
    def __str__(self):
        return f'{self.wide_size}x{self.heigth_size}_{self.material_print}_{self.post_obr}--{self.cost}'

    @staticmethod
    def get_wide_object(form_data):
        x = float(form_data['wide_size'])
        y = float(form_data['heigth_size'])
        material = Material.objects.get(id=int(form_data['material_print']))
        post_obr = Post_obr.objects.get(id=int(form_data['post_obr'])) 
        try:
            result = Wide.objects.get(wide_size=x,heigth_size=y, material_print=material, post_obr=post_obr)
            return result
        except ObjectDoesNotExist:
            cost = calc_cost(x,y,material,post_obr)
            new_wide_object = Wide(wide_size=x,heigth_size=y, material_print=material, post_obr=post_obr, cost=cost)
            new_wide_object.save()
            return new_wide_object
        
    def json_combine(self):
        json_dict = {'id': self.id,
                     'material': self.material_print.__str__(),
                     'x': self.wide_size,
                     'y': self.heigth_size,
                     'post_obr': self.post_obr.__str__(),
                     'cost': self.cost
                     }
        return json_dict



def calc_cost(*args):
    return 100000