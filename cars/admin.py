from django.contrib import admin
from django.utils.html import format_html
from .models import CarCategory, Car, CarSpecification, CarColor, CarImage


class CarSpecificationInline(admin.TabularInline):
    model = CarSpecification
    extra = 1
    fields = ['name', 'value', 'unit', 'order']


class CarColorInline(admin.TabularInline):
    model = CarColor
    extra = 1
    fields = ['name', 'hex_code', 'price_addition', 'image']


class CarImageInline(admin.TabularInline):
    model = CarImage
    extra = 1
    fields = ['image', 'alt_text', 'order']


@admin.register(CarCategory)
class CarCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'category_type', 'order']
    list_editable = ['order']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ['car_image_preview', 'name', 'category', 'price_display', 'status', 'is_featured', 'order']
    list_display_links = ['name']
    list_editable = ['status', 'is_featured', 'order']
    list_filter = ['category', 'status', 'is_featured']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [CarSpecificationInline, CarColorInline, CarImageInline]
    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('category', 'name', 'slug', 'subtitle', 'description', 'image')
        }),
        ('Narx', {
            'fields': ('base_price', 'discounted_price', 'discount_amount')
        }),
        ('Holat va ko\'rinish', {
            'fields': ('status', 'is_featured', 'order')
        }),
        ('URL', {
            'fields': ('url_path', 'online_buy_url'),
            'classes': ('collapse',)
        }),
    )

    def car_image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:50px;border-radius:4px;" />', obj.image.url)
        return "—"
    car_image_preview.short_description = "Rasm"

    def price_display(self, obj):
        price = obj.get_display_price()
        formatted = f"{price:,}".replace(",", " ")
        if obj.discounted_price:
            return format_html('<span style="color:green;font-weight:bold;">{} so\'m</span>', formatted)
        return f"{formatted} so'm"
    price_display.short_description = "Narx"
