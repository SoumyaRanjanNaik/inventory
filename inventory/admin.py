from django.contrib import admin

from inventory.models import Product, Sale, Stock, Bill, Restock

# Register your models here.

admin.site.register(Product)
admin.site.register(Sale)
admin.site.register(Stock)
admin.site.register(Bill)
admin.site.register(Restock)
