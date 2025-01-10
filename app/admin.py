from django.contrib import admin

from app.models import BillingAddress, Cart, CartItem, Customer, Product, SalesOrder, ShippingAddress, Promotion

# Register your models here.
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(ShippingAddress)
admin.site.register(BillingAddress)
admin.site.register(SalesOrder)
admin.site.register(Promotion)