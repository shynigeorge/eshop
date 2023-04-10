from django.contrib import admin

from cart.models import Cart, Items

admin.site.register(Cart)

class ItemsAdmin(admin.ModelAdmin):
    list_display = ['products', 'cart', 'quantity', 'active']

admin.site.register(Items,ItemsAdmin)