from django.contrib import admin

from .models import Snap_item, Snap_type, Stamp, Stamp_type

# Register your models here.

admin.site.register([Snap_item, Snap_type, Stamp, Stamp_type])
