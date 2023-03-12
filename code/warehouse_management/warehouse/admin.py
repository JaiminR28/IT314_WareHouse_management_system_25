from django.contrib import admin
from .models import Manager, Warehouse, Reservation, Crop_stored

# Register your models here.

admin.site.register(Manager)
admin.site.register(Warehouse)
admin.site.register(Reservation)
admin.site.register(Crop_stored)