from django.contrib import admin
from poly.models import Card_Model, Formats_Poly_Model, Leaflets_Model, Order_Model

# Register your models here.
admin.site.register([Card_Model, Leaflets_Model, Formats_Poly_Model, Order_Model])
