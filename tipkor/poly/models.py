from django.db import models

# Abstract class for poly


class MetaPoly(models.Model):
    PAPER_130 = 130
    PAPER_170 = 170
    PAPER_300 = 300
    PAPER_CHOICE = [(PAPER_130, '130 г/м'),
                    (PAPER_170, '170 г/м'),
                    (PAPER_300, '300 г/м'),]

    DUPLEX = [(True, '4+4'), (False, '4+0')]

    x = models.IntegerField(default=90, help_text='Горизонтальный размер')
    y = models.IntegerField(default=50, help_text='Вертикальный размер')
    paper = models.CharField(choices=PAPER_CHOICE, max_length=20, help_text='Плотность бумаги')
    pressrun = models.IntegerField(help_text='Тираж')
    duplex = models.BooleanField(default=True, choices=DUPLEX, help_text='Дуплекс')

    class Meta:
        abstract = True

class Cards(MetaPoly):
    PAPER_CHOICE = [(300, '300 г/м')]


    





