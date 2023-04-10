from django.contrib import admin

# Register your models here.
from order.models import Order, Itemorder, Profile

admin.site.register(Order)
admin.site.register(Itemorder)
admin.site.register(Profile)