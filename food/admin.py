from django.contrib import admin

from .models import Restaurant, Customer, Driver, Food, Order, OrderDetail

admin.site.register(Restaurant)
admin.site.register(Customer)
admin.site.register(Driver)
admin.site.register(Food)
admin.site.register(Order)
admin.site.register(OrderDetail)