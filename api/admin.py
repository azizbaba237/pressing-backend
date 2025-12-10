from django.contrib import admin
from api.models import *

# Register your models here.
admin.site.register(Service)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Payment)
