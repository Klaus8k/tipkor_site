from django.db import models

# Abstract class for poly


class MetaPoly(models.Model):
    PAPER_130 = "130"
    PAPER_170 = "170"
    PAPER_300 = "300"
    PAPER_CHOICE = [
        (PAPER_130, "130 г/м"),
        (PAPER_170, "170 г/м"),
        (PAPER_300, "300 г/м"),
    ]

    DUPLEX = [(True, "Двухсторонняя печать"), (False, "Односторонняя печать")]

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
        print(kwargs)
        if cls.objects.filter(**kwargs):
            return cls.objects.filter(**kwargs)[0]
        else: return 'No matching'

    class Meta:
        abstract = True


class Card_Model(MetaPoly):
    PAPER_CHOICE = [("300", "300 г/м"),]
    x = models.IntegerField(default=90, help_text="Горизонтальный размер")
    y = models.IntegerField(default=50, help_text="Вертикальный размер")
    paper = models.CharField(
        choices=PAPER_CHOICE, max_length=20, help_text="Плотность бумаги"
    )

class Formats_Poly_Model(models.Model):
    format_paper = models.CharField(max_length=20)
    x = models.IntegerField()
    y = models.IntegerField()

    def __str__(self):
        return f'{self.format_paper} - {self.x}x{self.y}'
    
class Leaflets_Model(MetaPoly):
    format_choice = models.ForeignKey(Formats_Poly_Model, on_delete=models.CASCADE)

    def __str__(self):
        x = self.format_choice
        print(x)
        return f'{x.format_paper} + {x.x} + {x.y} + {super().__str__()}'