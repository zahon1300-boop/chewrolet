from django.contrib import admin
from django.utils.html import format_html
from .models import TestDriveRequest, ContactRequest, CarOrder


@admin.register(TestDriveRequest)
class TestDriveRequestAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'phone', 'car', 'dealer', 'preferred_date', 'status', 'created_at']
    list_filter = ['status', 'car', 'dealer']
    list_editable = ['status']
    search_fields = ['full_name', 'phone', 'email']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'


@admin.register(ContactRequest)
class ContactRequestAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'phone', 'subject', 'status', 'created_at']
    list_filter = ['status']
    list_editable = ['status']
    search_fields = ['full_name', 'phone', 'email', 'subject']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'


@admin.register(CarOrder)
class CarOrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'full_name', 'phone', 'car', 'payment_type', 
                    'price_display', 'status', 'created_at']
    list_filter = ['status', 'payment_type', 'car', 'dealer']
    list_editable = ['status']
    search_fields = ['order_number', 'full_name', 'phone', 'passport']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'
    fieldsets = (
        ('Buyurtma', {'fields': ('order_number', 'status', 'notes')}),
        ('Mijoz', {'fields': ('full_name', 'phone', 'email', 'passport')}),
        ('Avtomobil', {'fields': ('car', 'color', 'dealer')}),
        ('To\'lov', {'fields': ('payment_type', 'total_price', 'down_payment')}),
        ('Sana', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )

    def price_display(self, obj):
        formatted = f"{obj.total_price:,}".replace(",", " ")
        return f"{formatted} so'm"
    price_display.short_description = "Narx"
