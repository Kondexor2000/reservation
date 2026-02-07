from django.contrib import admin
from .models import Category, Order, NumberPhone

# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'categories_list']

    def categories_list(self, obj):
        return ", ".join([c.name for c in obj.category.all()])

    categories_list.short_description = "Kategorie"

class NumberPhoneAdmin(admin.ModelAdmin):
    list_display = ['user', 'number_phone']

admin.site.register(Category, CategoryAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(NumberPhone, NumberPhoneAdmin)