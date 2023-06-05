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

    DUPLEX = [(True, "4+4"), (False, "4+0")]

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
        return "{}x{}, {}г/м, {}, {}шт - {}руб".format(
            self.x, self.y, self.paper, duplex, self.pressrun, self.cost
        )

    class Meta:
        abstract = True


class Card_Model(MetaPoly):
    x = models.IntegerField(default=90, help_text="Горизонтальный размер")
    y = models.IntegerField(default=50, help_text="Вертикальный размер")
    paper = models.CharField(
        choices=[("300", "300 г/м")],
        default="300",
        max_length=20,
        help_text="Плотность бумаги",
    )

class Formats_Poly_Model(models.Model):
    format_paper = models.CharField(max_length=5)
    x = models.IntegerField()
    y = models.IntegerField()

    def __str__(self):
        return self.format_paper
    
class Leaflets_Model(MetaPoly):
    format_choice = models.ForeignKey(Formats_Poly_Model, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.format_choice.format_paper) + super().__str__()[4:]
