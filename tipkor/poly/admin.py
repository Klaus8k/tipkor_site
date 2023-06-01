from django.contrib import admin
from poly.models import Cards, Leaflets, FormatsPoly

# Register your models here.
admin.site.register([Cards, Leaflets, FormatsPoly])