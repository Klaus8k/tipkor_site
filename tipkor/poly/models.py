from datetime import datetime

from django.db import models


class Formats_Model(models.Model):
    """" Класс форматов бумаги
    Атрибуты: Название, ширина, высота бумаги
    """
    format_paper = models.CharField(max_length=20)
    x = models.IntegerField()
    y = models.IntegerField()

    def __str__(self):
        return f'{self.format_paper} ({self.x}x{self.y}мм)'

class MetaPoly(models.Model):
    """ Мета класс для полиграфии
    """
    FORMAT = None
    PAPER_CHOICE = [
        ("130", "130 г/м"),
        ("170", "170 г/м"),
        ("300", "300 г/м"),
    ]
    DUPLEX = [(True, "Двухсторонняя печать"), (False, "Односторонняя печать")]
    
    format = models.ForeignKey(Formats_Model, null=True, on_delete=models.CASCADE)
    paper = models.CharField(default='130', choices=PAPER_CHOICE, max_length=20)
    pressrun = models.IntegerField()
    duplex = models.BooleanField(default=True, choices=DUPLEX)
    cost = models.IntegerField(null=True)

    def __str__(self) -> str:
        duplex = "4+0"
        if self.duplex:
            duplex = "4+4"
        return "{}, {}г/м, {}, {}шт - {} руб.".format(
            self.format, self.paper, duplex, self.pressrun, self.cost
        )

    @classmethod
    def get_cost(cls, **kwargs): 
        """ Метод возврата цены 
            пробует взять обеъект из базы по словарю
            елси есть возвращает цену (пока весь объкт)
            и передает словарь с ценой на запись в заказы"""
        order_dict = kwargs.copy()
        del order_dict['type_production']
        try:
            order_set = cls.objects.get(**order_dict)
        except:
            return 'No matching'
        kwargs.update({'cost': order_set.cost})
        Order_Model.save_calculation(**kwargs)
        return order_set

    class Meta:
        abstract = True

# Модель списка расчетов 
class Order_Model(models.Model):
    date_create = models.DateTimeField(auto_now_add=True, null=True)
    type_production = models.CharField(max_length=20, null=True)
    production = models.CharField(max_length=100, null=True)
    time_ready = models.DateTimeField(null=True)
    cost = models.IntegerField(null=True)

    def save_calculation(**kwargs):   
        """ собирает словарь для добавления в базу, еще дату надо"""
        dict_to_save = {
            'type_production': kwargs['type_production'],
            'production': f"{kwargs['pressrun']}, \
                            {Formats_Model.objects.get(id=kwargs['format'])} \
                            {kwargs['paper']}г/м", 
            'cost': kwargs['cost'],
            # 'time_ready': 
        }
        order = Order_Model(**dict_to_save)
        order.save()

    def __str__(self) -> str:
        return f'{self.type_production} - {self.production}'

    def date_to_ready(self):
        """Метод возврата даты готовности"""
        pass


# Класс для визиток
class Card_Model(MetaPoly):
    PAPER_CHOICE = [("300", "300 г/м"),]
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)


# класс листовок
class Leaflets_Model(MetaPoly):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

class Booklet_Model(MetaPoly):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)