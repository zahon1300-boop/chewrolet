from django.contrib import admin
from django.utils.html import format_html
from .models import NewsCategory, News, SpecialOffer


@admin.register(NewsCategory)
class NewsCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['news_image', 'title', 'category', 'is_published', 'is_slider', 'published_at']
    list_display_links = ['title']
    list_editable = ['is_published', 'is_slider']
    list_filter = ['is_published', 'is_slider', 'category']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_at'

    def news_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:40px;border-radius:4px;" />', obj.image.url)
        return "—"
    news_image.short_description = "Rasm"


@admin.register(SpecialOffer)
class SpecialOfferAdmin(admin.ModelAdmin):
    list_display = ['title', 'car', 'bank_name', 'interest_rate', 'is_active', 'valid_until']
    list_filter = ['is_active', 'car']
    list_editable = ['is_active']
    search_fields = ['title', 'bank_name']
