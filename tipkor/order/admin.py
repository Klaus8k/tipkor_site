from django.contrib import admin
from order.models import Clients, Orders


# Register your models here.
@admin.register(Orders)
class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ('create_date',)

admin.site.register(Clients)
