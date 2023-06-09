import json

from django.core.exceptions import ValidationError
from django.db import models
from order.models import Orders

from .constants import DUPLEX, PAPER_CHOICE, BOOKLETS


def valid(value):
    if isinstance(value % 1000, int):
        raise ValidationError('должно быть кратно 1000')

class Formats(models.Model):
    """" Класс форматов бумаги
    Атрибуты: Название, ширина, высота бумаги
    """
    format_p = models.CharField(max_length=20, null=True, blank=True)
    x = models.IntegerField()
    y = models.IntegerField()

    def __str__(self):
        if self.format_p:
            return f'{self.format_p} ({self.x}x{self.y}мм)'
        else:
            return '{}x{}'.format(self.x, self.y)

class Poly(models.Model):
    format_p = models.ForeignKey(Formats,on_delete=models.DO_NOTHING)
    paper = models.CharField(choices=PAPER_CHOICE, max_length=20)
    pressrun = models.IntegerField()
    duplex = models.BooleanField(choices=DUPLEX, max_length=50, default=True)
    post_obr = models.CharField(null=True, blank=True, choices=BOOKLETS, max_length=20)
    cost = models.IntegerField()

    def __str__(self):
        return f'{self.format_p}, {self.paper}г/м ,{self.pressrun}шт.,4+4 - {self.duplex}, post:{self.post_obr} = {self.cost}руб.'

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



