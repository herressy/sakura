from django.contrib import admin
from .models import User, Table, Order, Meal

class OrderInline(admin.StackedInline):
    model = Order
    extra = 10

class TableAdmin(admin.ModelAdmin):
    inlines = [OrderInline]

admin.site.register(User)
admin.site.register(Table, TableAdmin)
admin.site.register(Order)
admin.site.register(Meal)