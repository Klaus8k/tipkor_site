from django.db import models


# класс форматов
class Formats_Poly_Model(models.Model):
    format_paper = models.CharField(max_length=20)
    x = models.IntegerField()
    y = models.IntegerField()

    def __str__(self):
        return f'{self.format_paper} - {self.x}x{self.y}мм'

# Мета класс для полиграфии. с расчетом
class MetaPoly(models.Model):

    FORMAT = None
    PAPER_CHOICE = [
        ("130", "130 г/м"),
        ("170", "170 г/м"),
        ("300", "300 г/м"),
    ]
    DUPLEX = [(True, "Двухсторонняя печать"), (False, "Односторонняя печать")]
    
    format = models.ForeignKey(Formats_Poly_Model, null=True, on_delete=models.CASCADE)

    # format = models.CharField(
    #     choices=FORMAT, max_length=20, help_text="Формат"
    # )
    paper = models.CharField(
        choices=PAPER_CHOICE, max_length=20, help_text="Плотность бумаги"
    )
    pressrun = models.IntegerField(help_text="Тираж")
    duplex = models.BooleanField(default=True, choices=DUPLEX, help_text="Дуплекс")
    cost = models.IntegerField(null=True, help_text="Цена")

    def __str__(self) -> str:
        duplex = "4+0"
        if self.duplex:
            duplex = "4+4"
        return "{}г/м, {}, {}шт - {} руб.".format(
            self.paper, duplex, self.pressrun, self.cost
        )

    @classmethod
    def save_calculation(cls, **kwargs):
        Order_Model.save_calculation(**kwargs)
    
    @classmethod
    def get_cost(cls, **kwargs): 
        type_production = kwargs.pop('type_production')
        try:
            order_set = cls.objects.get(**kwargs)
            kwargs_to_save = {'type_production':type_production,
                               'production' : order_set,
                               'cost': order_set.cost
                                }
            cls.save_calculation(**kwargs_to_save)
            return order_set
        except:
            return 'No matching'

    class Meta:
        abstract = True

# Модель списка расчетов 
class Order_Model(models.Model):
    date_create = None
    type_production = models.CharField(max_length=20, null=True)
    production = models.CharField(max_length=100, null=True)
    date_to_ready = None
    cost = models.IntegerField(null=True)

    @classmethod
    def save_calculation(cls, **kwargs):
        order = cls(**kwargs)
        order.save()

    def __str__(self) -> str:
        return f'{self.type_production} - {self.production}'


# Класс для визиток
class Card_Model(MetaPoly):

    def __str__(self):
        x = self.format
        return f'{x.format_paper}, {self.duplex}, {self.pressrun} = {self.cost}'

# класс листовок
class Leaflets_Model(MetaPoly):

    # format = models.ForeignKey(Formats_Poly_Model, on_delete=models.CASCADE)

    def __str__(self):
        x = self.format
        return f'{x.format_paper} + {x.x} + {x.y} + {super().__str__()}'