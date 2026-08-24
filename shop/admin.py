from django.contrib import admin
from .models import Product, Order, OrderItem


# ثبت مدل‌ها در پنل مدیریت Django
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)