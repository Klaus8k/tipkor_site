import datetime
import json

from django.core.exceptions import ValidationError
from django.db import models
from order.models import Orders

from .constants import DUPLEX, PAPER_CHOICE


def valid(value):
    if isinstance(value % 1000, int):
        raise ValidationError('должно быть кратно 1000')

class Formats(models.Model):
    """" Класс форматов бумаги
    Атрибуты: Название, ширина, высота бумаги
    """
    format_p = models.CharField(max_length=20)
    x = models.IntegerField()
    y = models.IntegerField()

    def __str__(self):
        return f'{self.format_p} ({self.x}x{self.y}мм)'

class Poly(models.Model):
    format_p = models.ForeignKey(Formats,on_delete=models.DO_NOTHING)
    paper = models.CharField(choices=PAPER_CHOICE, max_length=20)
    pressrun = models.IntegerField()
    duplex = models.BooleanField(choices=DUPLEX, max_length=50, default=True)
    post_obr = models.JSONField(null=True, blank=True)
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


def date_to_ready():
    """Расчитывает дату готовности. Если после 15-00 и до 9-00 то + 1 день.
    Если на выходные попадает то до близжайшего понедельника переносится дата
    work_time - Времы работы над заказом
    Returns:
        date: Дата готовности заказа
    """
    work_time = 1
    time_create = datetime.datetime.now()
    if time_create.hour > 15 or time_create.hour < 9: # если заказ после 15-00 то +1 день на работу
        work_time += 1
    time_ready = time_create + datetime.timedelta(days=work_time)
    if time_ready.weekday() >= 5: # если на субботу или воскресенье попадает - переносится на понедельник готовность.
        while time_ready.weekday() != 0:
            time_ready += datetime.timedelta(days=1)
    return time_ready
