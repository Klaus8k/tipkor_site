from django.db import models


# Мета класс для полиграфии. с расчетом
class MetaPoly(models.Model):

    TYPE_PRODUCTION = None
    
    PAPER_130 = "130"
    PAPER_170 = "170"
    PAPER_300 = "300"
    PAPER_CHOICE = [
        (PAPER_130, "130 г/м"),
        (PAPER_170, "170 г/м"),
        (PAPER_300, "300 г/м"),
    ]

    DUPLEX = [(True, "Двухсторонняя печать"), (False, "Односторонняя печать")]

    type_production = models.CharField(max_length=20)
    x = models.IntegerField(blank=True, null=True, help_text="Горизонтальный размер")
    y = models.IntegerField(blank=True, null=True, help_text="Вертикальный размер")
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
        return "{}x{}, {}г/м, {}, {}шт - {} руб.".format(
            self.x, self.y, self.paper, duplex, self.pressrun, self.cost
        )
    
    @classmethod
    def get_cost(cls, **kwargs): 
        Order_Model.record_order(**kwargs)
        order_set = cls.objects.filter(**kwargs)
        print(order_set)

        if cls.objects.filter(**kwargs):
            return cls.objects.filter(**kwargs)[0]
        else: return 'No matching'

    class Meta:
        abstract = True

# класс заказов (дата создания, что это, расчет из вида заказа, готовность)
class Order_Model(models.Model):
    date_create = None
    type_production = models.CharField(max_length=20, null=True)
    production = models.CharField(max_length=100, null=True)
    date_to_ready = None


    @classmethod
    def record_order(cls, *args, **kwargs):
        type_production = kwargs.pop('type_production')
        order = cls(
                type_production=type_production,
                production = kwargs,
                    )
        order.save()

# класс форматов
class Formats_Poly_Model(models.Model):
    format_paper = models.CharField(max_length=20)
    x = models.IntegerField()
    y = models.IntegerField()

    def __str__(self):
        return f'{self.format_paper} - {self.x}x{self.y}мм'

# Класс для визиток
class Card_Model(MetaPoly):
    
    PAPER_CHOICE = [("300", "300 г/м"),]
    TYPE_PRODUCTION = 'card'

    type_production = models.CharField(max_length=20, default=TYPE_PRODUCTION)
    x = models.IntegerField(default=90, help_text="Горизонтальный размер")
    y = models.IntegerField(default=50, help_text="Вертикальный размер")
    paper = models.CharField(
        choices=PAPER_CHOICE, max_length=20, help_text="Плотность бумаги"
    )


# класс листовок
class Leaflets_Model(MetaPoly):
    TYPE_PRODUCTION = 'leaflet'

    type_production = models.CharField(max_length=20, default=TYPE_PRODUCTION)
    format_choice = models.ForeignKey(Formats_Poly_Model, on_delete=models.CASCADE)

    def __str__(self):
        x = self.format_choice
        return f'{x.format_paper} + {x.x} + {x.y} + {super().__str__()}'