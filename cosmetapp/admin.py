from django.contrib import admin
from .models import Category, Order, NumberPhone

# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'category']

class NumberPhoneAdmin(admin.ModelAdmin):
    list_display = ['user', 'number_phone']

admin.site.register(Category, CategoryAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(NumberPhone, NumberPhoneAdmin)