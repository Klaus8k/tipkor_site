from django.db import models


class Clients(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    tel = models.CharField(max_length=15)
    
    def __str__(self):
        return f'{self.name} - e-mail:{self.email} tel: {self.tel}'

# Create your models here.
class Orders(models.Model):
    client = models.ForeignKey(Clients, on_delete=models.DO_NOTHING)
    create_date = models.DateTimeField(auto_now=True)
    product = models.JSONField(null=True, blank=True)
    ready_date = models.DateField(null=True, blank=True)
    pay_info = models.BooleanField(null=True, blank=True)
    file = models.FileField(null=True, blank=True)
    
    def __str__(self):
        return f'{self.client} - {self.create_date}'
    