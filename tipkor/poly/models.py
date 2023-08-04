import json


from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import models
from order.models import Orders
from django.utils.translation import gettext_lazy

from .constants import BOOKLETS, DUPLEX, PAPER_CHOICE

def validate_int_size(value):
    if value < 30 or value > 630:
        raise ValidationError(
            gettext_lazy('%(value) размер должен быть больше 30мм и меньше 630мм'),
                    params={'value': value},
                        )



class Formats(models.Model):
    """" Класс форматов бумаги
    Атрибуты: Название, ширина, высота бумаги
    """
    format_p = models.CharField(max_length=20, null=True, blank=True)
    x = models.IntegerField(validators=[validate_int_size])
    y = models.IntegerField(validators=[validate_int_size])

    def __str__(self):
        if self.format_p:
            return f'{self.format_p} ({self.x}x{self.y}мм)'
        else:
            return '{}x{}'.format(self.x, self.y)

class Poly(models.Model):
    format_p = models.ForeignKey(Formats,on_delete=models.CASCADE)
    paper = models.CharField(choices=PAPER_CHOICE, max_length=20)
    pressrun = models.IntegerField()
    duplex = models.BooleanField(choices=DUPLEX, max_length=50, default=True)
    post_obr = models.CharField(choices=BOOKLETS, blank=True, null=True, max_length=20)
    cost = models.IntegerField()

    def __str__(self):
        return f'{self.format_p}, {self.paper}г/м ,{self.pressrun}шт.,4+4 - {self.duplex}, post:{self.post_obr} = {self.cost}руб.'
    
    @staticmethod
    def get_poly_object(data_form):
        try:
            result = Poly.objects.get(**data_form)
            result.cost = multiply_cost(result.cost, result.pressrun)
            return result
        except: #TODO Нет строки в бд, попробовать с парсера (это на потом)

            return {'cost': 'Неверные параметры расчета'}

    def json_combine(self):
        json_dict = {'id': self.id,
                     'format_p': self.format_p.__str__(),
                     'paper': self.paper,
                     'pressrun': self.pressrun,
                     'duplex': self.duplex,
                     'post_obr': self.post_obr,
                     'cost': self.cost
                     }
        return json_dict



def multiply_cost(cost: int, pressrun: int):
    if pressrun < 500:
        marge = 400
        return ((cost + marge) // 10 + 1) * 10
    elif pressrun == 500:
        marge = 1000
        return ((cost + marge) // 10 + 1) * 10
    elif pressrun == 1000:
        marge = 1200
        return ((cost + marge) // 10 + 1) * 10
    else:
        return ((cost * 1.46) // 10 + 1) * 10
        