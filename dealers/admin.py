from django.contrib import admin
from .models import Region, Dealer, ServiceCenter


class ServiceCenterInline(admin.TabularInline):
    model = ServiceCenter
    extra = 1
    fields = ['name', 'address', 'phone', 'is_active']


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ['name', 'order']
    list_editable = ['order']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Dealer)
class DealerAdmin(admin.ModelAdmin):
    list_display = ['name', 'region', 'market_type', 'phone', 'is_active']
    list_filter = ['region', 'market_type', 'is_active']
    search_fields = ['name', 'address', 'phone']
    list_editable = ['is_active']
    inlines = [ServiceCenterInline]
    fieldsets = (
        ('Asosiy', {'fields': ('name', 'region', 'market_type', 'is_active', 'order')}),
        ('Aloqa', {'fields': ('address', 'phone', 'phone2', 'email', 'website', 'working_hours')}),
        ('Xarita', {'fields': ('latitude', 'longitude'), 'classes': ('collapse',)}),
    )
