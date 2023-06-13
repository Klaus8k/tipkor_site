import datetime

from django.db import models

DATE_TO_STR = "%H:%M - %m/%d"

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
            order_result = cls.objects.get(**order_dict)
        except:
            return 'No matching'
        kwargs.update({'cost': order_result.cost})
        
        Order_Model.save_calculation(**kwargs)
        return order_result

    class Meta:
        abstract = True

# Модель списка расчетов 
class Order_Model(models.Model):
    date_create = models.DateTimeField(auto_now_add=True)
    type_production = models.CharField(max_length=20, null=True)
    production = models.CharField(max_length=100, null=True)
    time_ready = models.DateTimeField(null=True)
    cost = models.IntegerField(null=True)

    @classmethod
    def save_calculation(cls, **kwargs):   
        """ собирает словарь для добавления в базу"""
        format = Formats_Model.objects.get(id=kwargs['format'])
        time_ready = cls.date_to_ready()
        dict_to_save = {
            'type_production': kwargs['type_production'],
            'production': f"{kwargs['pressrun']}шт., {format}, {kwargs['paper']}г/м",
            'cost': kwargs['cost'],
            'time_ready': time_ready,
        }
        order = Order_Model(**dict_to_save)
        order.save()

    def __str__(self) -> str: 
        return f'{self.date_create.strftime(DATE_TO_STR)} {self.type_production} {self.production} {self.cost} готовность: {self.time_ready.date()}'


    @staticmethod
    def date_to_ready():
        """Метод возврата даты готовности
        work_time - стандартное время на работу"""
        work_time = 1
        time_create = datetime.datetime.now()
        if time_create.hour > 15: # если заказ после 15-00 то +1 день на работу
            work_time += 1
        time_ready = time_create + datetime.timedelta(days=work_time)
        if time_ready.weekday() >= 5: # если на субботу или воскресенье попадает - переносится на понедельник готовность.
            while time_ready.weekday() != 0:
                time_ready += datetime.timedelta(days=1)
        return time_ready


# Класс для визиток
class Card_Model(MetaPoly):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

# класс листовок
class Leaflets_Model(MetaPoly):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

class Booklet_Model(MetaPoly):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)