from django.contrib import admin
from order.models import Clients, Orders

# Register your models here.
admin.site.register([Orders, Clients])
