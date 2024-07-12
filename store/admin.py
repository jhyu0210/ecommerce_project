from jmespath import search
from django.contrib import admin


# Register your models here.
from .models import Category, Order, OrderItem,Product

admin.site.register(Category)
admin.site.register(Product)

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

class OrderAdmin(admin.ModelAdmin):
    list_display=['id','is_paid','created_at']
    list_filter=['is_paid','created_at','created_by']
    search_fields = ['first_name','address']
    inlines = [OrderItemInline]

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)