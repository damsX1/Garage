from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(UserSettings)
admin.site.register(Customer)
admin.site.register(CarModel)
admin.site.register(Vehicle)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Invoice)
admin.site.register(InvoiceItem)