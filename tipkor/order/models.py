from django.db import models


class Clients(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    tel = models.CharField(max_length=15)

# Create your models here.
class Orders(models.Model):
    client = models.ForeignKey(Clients, on_delete=models.DO_NOTHING)
    create_date = models.DateTimeField()
    poduct = models.JSONField()
    ready_date = models.DateField()
    pay_info = models.BooleanField()
    file = models.FileField()
    