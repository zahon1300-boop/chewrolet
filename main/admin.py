"""
main/admin.py — Professional Django Admin konfiguratsiyasi.

Qidiruv, filterlar, thumbnail preview va boshqa kengaytirilgan
imkoniyatlar bilan to'liq sozlangan admin panel.
"""

from __future__ import annotations

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.db.models import Count, QuerySet
from django.http import HttpRequest
from django.utils.html import format_html
from django.utils.safestring import SafeText

from main.models import (
    Car,
    CarBrand,
    CarCategory,
    CarImage,
    News,
    NewsCategory,
    UserProfile,
)

User = get_user_model()


# ==============================================================================
# YORDAMCHI METODLAR
# ==============================================================================

def thumbnail_html(image_field, width: int = 60, height: int = 40) -> SafeText:
    """
    Rasm maydoni uchun HTML thumbnail generatsiya qiladi.

    Args:
        image_field: ImageField ob'ekti
        width: Thumbnail kengligi
        height: Thumbnail balandligi

    Returns:
        Xavfsiz HTML string
    """
    if image_field:
        return format_html(
            '<img src="{}" width="{}" height="{}" '
            'style="object-fit:cover; border-radius:4px; '
            'border:1px solid #ddd;" />',
            image_field.url,
            width,
            height,
        )
    return format_html(
        '<span style="color:#999; font-size:11px;">Rasm yo\'q</span>'
    )


# ==============================================================================
# BREND
# ==============================================================================

@admin.register(CarBrand)
class CarBrandAdmin(admin.ModelAdmin):
    """Avtomobil brendlari admin paneli."""

    list_display = ("name", "logo_preview", "cars_count", "slug")
    list_display_links = ("name",)
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ("logo_preview_large",)

    fieldsets = (
        ("Asosiy ma'lumotlar", {
            "fields": ("name", "slug", "description"),
        }),
        ("Logotip", {
            "fields": ("logo", "logo_preview_large"),
        }),
    )

    @admin.display(description="Logotip")
    def logo_preview(self, obj: CarBrand) -> SafeText:
        return thumbnail_html(obj.logo, 50, 35)

    @admin.display(description="Logotip (katta)")
    def logo_preview_large(self, obj: CarBrand) -> SafeText:
        return thumbnail_html(obj.logo, 200, 140)

    @admin.display(description="Avtomobillar soni")
    def cars_count(self, obj: CarBrand) -> int:
        return obj.cars.count()

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        return super().get_queryset(request).annotate(
            _cars_count=Count("cars", distinct=True)
        )


# ==============================================================================
# KATEGORIYA
# ==============================================================================

@admin.register(CarCategory)
class CarCategoryAdmin(admin.ModelAdmin):
    """Avtomobil kategoriyalari admin paneli."""

    list_display = ("name", "icon_class", "cars_count", "slug")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}

    @admin.display(description="Avtomobillar soni")
    def cars_count(self, obj: CarCategory) -> int:
        return obj.cars.count()


# ==============================================================================
# AVTOMOBIL RASMLARI (Inline)
# ==============================================================================

class CarImageInline(admin.TabularInline):
    """Avtomobil rasmlari uchun inline forma."""

    model = CarImage
    extra = 3
    fields = ("image", "image_preview", "is_main", "order", "alt_text", "caption")
    readonly_fields = ("image_preview",)
    ordering = ("-is_main", "order")

    @admin.display(description="Ko'rinish")
    def image_preview(self, obj: CarImage) -> SafeText:
        return thumbnail_html(obj.image, 80, 55)


# ==============================================================================
# AVTOMOBIL
# ==============================================================================

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    """
    Avtomobil admin paneli.

    Kengaytirilgan qidiruv, filterlar va thumbnail preview bilan.
    """

    list_display = (
        "main_image_preview",
        "name",
        "brand",
        "category",
        "model_year",
        "price_display",
        "transmission",
        "is_active",
        "is_featured",
        "views_count",
        "created_at",
    )
    list_display_links = ("name",)
    list_filter = (
        "brand",
        "category",
        "is_active",
        "is_featured",
        "is_new",
        "transmission",
        "drive_type",
        "fuel_type",
        "model_year",
    )
    search_fields = ("name", "slug", "short_description", "color")
    prepopulated_fields = {"slug": ("name", "model_year")}
    readonly_fields = (
        "main_image_preview",
        "views_count",
        "created_at",
        "updated_at",
    )
    date_hierarchy = "created_at"
    list_per_page = 25
    list_editable = ("is_active", "is_featured")
    ordering = ("-created_at",)
    inlines = [CarImageInline]

    fieldsets = (
        ("📋 Asosiy ma'lumotlar", {
            "fields": (
                "brand", "category", "name", "model_year", "slug",
                "short_description", "full_description",
                "is_active", "is_featured", "is_new", "color",
            ),
        }),
        ("💰 Narx", {
            "fields": ("price", "price_uzs", "is_price_negotiable"),
        }),
        ("⚙️ Dvigatel", {
            "fields": (
                "engine_volume", "engine_power_hp", "engine_power_kw",
                "engine_torque", "fuel_type",
                "fuel_consumption_city", "fuel_consumption_highway",
            ),
            "classes": ("collapse",),
        }),
        ("🔧 Uzatmalar va yurish tizimi", {
            "fields": ("transmission", "gears_count", "drive_type"),
            "classes": ("collapse",),
        }),
        ("📐 O'lchamlar va dinamika", {
            "fields": (
                "length_mm", "width_mm", "height_mm", "wheelbase_mm",
                "curb_weight_kg", "trunk_volume_l", "fuel_tank_l",
                "acceleration_0_100", "max_speed",
            ),
            "classes": ("collapse",),
        }),
        ("📊 Statistika", {
            "fields": ("views_count", "created_at", "updated_at"),
        }),
    )

    @admin.display(description="Asosiy rasm")
    def main_image_preview(self, obj: Car) -> SafeText:
        main_img = obj.images.filter(is_main=True).first() or obj.images.first()
        if main_img:
            return thumbnail_html(main_img.image, 70, 48)
        return format_html('<span style="color:#999">—</span>')

    @admin.display(description="Narx", ordering="price")
    def price_display(self, obj: Car) -> str:
        return f"${obj.price:,.0f}"

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        return super().get_queryset(request).select_related(
            "brand", "category"
        ).prefetch_related("images")


# ==============================================================================
# YANGILIKLAR
# ==============================================================================

@admin.register(NewsCategory)
class NewsCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    """
    Yangiliklar admin paneli.

    Nashr holati, muqova ko'rinishi va statistika bilan.
    """

    list_display = (
        "cover_preview",
        "title",
        "category",
        "is_published",
        "is_featured",
        "views_count",
        "published_at",
    )
    list_display_links = ("title",)
    list_filter = (
        "is_published",
        "is_featured",
        "category",
        ("published_at", admin.DateFieldListFilter),
    )
    search_fields = ("title", "slug", "excerpt", "content")
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = (
        "cover_preview_large",
        "views_count",
        "created_at",
        "updated_at",
    )
    date_hierarchy = "published_at"
    list_per_page = 20
    list_editable = ("is_published", "is_featured")
    ordering = ("-created_at",)

    fieldsets = (
        ("📰 Asosiy ma'lumotlar", {
            "fields": (
                "category", "title", "slug", "excerpt", "content",
                "related_car",
            ),
        }),
        ("🖼️ Muqova rasmi", {
            "fields": ("cover_image", "cover_preview_large"),
        }),
        ("📢 Nashr holati", {
            "fields": ("is_published", "is_featured", "published_at"),
        }),
        ("📊 Statistika", {
            "fields": ("views_count", "created_at", "updated_at"),
        }),
    )

    @admin.display(description="Rasm")
    def cover_preview(self, obj: News) -> SafeText:
        return thumbnail_html(obj.cover_image, 80, 50)

    @admin.display(description="Muqova rasmi (katta)")
    def cover_preview_large(self, obj: News) -> SafeText:
        return thumbnail_html(obj.cover_image, 300, 200)


# ==============================================================================
# FOYDALANUVCHI PROFILI (Inline va alohida)
# ==============================================================================

class UserProfileInline(admin.StackedInline):
    """Foydalanuvchi sahifasiga profil inline sifatida qo'shish."""

    model = UserProfile
    can_delete = False
    verbose_name = "Profil"
    verbose_name_plural = "Profil ma'lumotlari"
    readonly_fields = ("avatar_preview", "created_at", "updated_at")
    extra = 0

    fieldsets = (
        (None, {
            "fields": (
                "avatar", "avatar_preview",
                "bio", "phone", "address", "city", "date_of_birth",
            ),
        }),
    )

    @admin.display(description="Avatar ko'rinishi")
    def avatar_preview(self, obj: UserProfile) -> SafeText:
        return thumbnail_html(obj.avatar, 60, 60)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """Foydalanuvchi profillari admin paneli."""

    list_display = (
        "avatar_preview",
        "user",
        "get_full_name",
        "phone",
        "city",
        "created_at",
    )
    list_display_links = ("user",)
    search_fields = (
        "user__username",
        "user__first_name",
        "user__last_name",
        "user__email",
        "phone",
        "city",
    )
    list_filter = ("city", "created_at")
    readonly_fields = ("avatar_preview_large", "created_at", "updated_at")
    ordering = ("-created_at",)

    fieldsets = (
        ("👤 Foydalanuvchi", {
            "fields": ("user",),
        }),
        ("🖼️ Avatar", {
            "fields": ("avatar", "avatar_preview_large"),
        }),
        ("📋 Shaxsiy ma'lumotlar", {
            "fields": ("bio", "date_of_birth"),
        }),
        ("📞 Aloqa", {
            "fields": ("phone", "address", "city"),
        }),
        ("📊 Tizim", {
            "fields": ("created_at", "updated_at"),
        }),
    )

    @admin.display(description="Avatar")
    def avatar_preview(self, obj: UserProfile) -> SafeText:
        return thumbnail_html(obj.avatar, 45, 45)

    @admin.display(description="Avatar (katta)")
    def avatar_preview_large(self, obj: UserProfile) -> SafeText:
        return thumbnail_html(obj.avatar, 150, 150)

    @admin.display(description="To'liq ism", ordering="user__first_name")
    def get_full_name(self, obj: UserProfile) -> str:
        return obj.user.get_full_name() or "—"


# ==============================================================================
# USER ADMIN KENGAYTIRISH (Profil Inline bilan)
# ==============================================================================

class CustomUserAdmin(BaseUserAdmin):
    """Django User admin paneliga profil inline ni qo'shadi."""

    inlines = (*BaseUserAdmin.inlines, UserProfileInline)


# Mavjud User admin ni qayta ro'yxatdan o'tkazish
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


# ==============================================================================
# HERO BANNER ADMIN
# ==============================================================================
from main.models import HeroBanner

@admin.register(HeroBanner)
class HeroBannerAdmin(admin.ModelAdmin):
    """Hero banner admin paneli — rasm preview va tartib boshqaruvi."""

    list_display = ("banner_preview", "title", "order", "is_active", "created_at")
    list_display_links = ("title",)
    list_editable = ("order", "is_active")
    list_per_page = 20
    readonly_fields = ("banner_preview_large", "created_at")

    fieldsets = (
        ("🖼️ Rasm", {
            "fields": ("image", "banner_preview_large"),
        }),
        ("📝 Matn", {
            "fields": ("title", "subtitle"),
        }),
        ("🔗 Tugma", {
            "fields": ("button_text", "button_url"),
        }),
        ("⚙️ Sozlamalar", {
            "fields": ("is_active", "order", "created_at"),
        }),
    )

    @admin.display(description="Ko'rinish")
    def banner_preview(self, obj: HeroBanner) -> SafeText:
        return thumbnail_html(obj.image, 120, 60)

    @admin.display(description="Banner rasmi (katta ko'rinish)")
    def banner_preview_large(self, obj: HeroBanner) -> SafeText:
        return thumbnail_html(obj.image, 600, 280)
