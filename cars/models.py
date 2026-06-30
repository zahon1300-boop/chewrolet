from django.db import models
from django.utils.translation import gettext_lazy as _


class CarCategory(models.Model):
    CATEGORY_CHOICES = [
        ('suv', 'SUV'),
        ('sedan', 'Sedan / Cars'),
        ('lcv', 'LCV (Yengil tijorat)'),
    ]
    name = models.CharField(max_length=100, verbose_name="Kategoriya nomi")
    slug = models.SlugField(unique=True)
    category_type = models.CharField(max_length=20, choices=CATEGORY_CHOICES, verbose_name="Turi")
    order = models.PositiveIntegerField(default=0, verbose_name="Tartib")

    class Meta:
        verbose_name = "Kategoriya"
        verbose_name_plural = "Kategoriyalar"
        ordering = ['order']

    def __str__(self):
        return self.name


class Car(models.Model):
    STATUS_CHOICES = [
        ('active', 'Faol'),
        ('soon', 'Tez Kunda'),
        ('discontinued', 'To\'xtatilgan'),
    ]

    category = models.ForeignKey(CarCategory, on_delete=models.SET_NULL, null=True, verbose_name="Kategoriya")
    name = models.CharField(max_length=100, verbose_name="Model nomi")
    slug = models.SlugField(unique=True)
    subtitle = models.CharField(max_length=255, blank=True, verbose_name="Qo'shimcha nom")
    description = models.TextField(blank=True, verbose_name="Tavsif")
    image = models.ImageField(upload_to='cars/', blank=True, verbose_name="Rasm")
    
    base_price = models.BigIntegerField(verbose_name="Boshlang'ich narx (so'm)")
    discounted_price = models.BigIntegerField(null=True, blank=True, verbose_name="Chegirma narxi (so'm)")
    discount_amount = models.BigIntegerField(null=True, blank=True, verbose_name="Chegirma miqdori (so'm)")

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active', verbose_name="Holat")
    is_featured = models.BooleanField(default=False, verbose_name="Bosh sahifada ko'rsatish")
    order = models.PositiveIntegerField(default=0, verbose_name="Tartib")

    url_path = models.CharField(max_length=100, blank=True, verbose_name="Sayt URL yo'li")
    online_buy_url = models.URLField(blank=True, verbose_name="Onlayn xarid URL")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Avtomobil"
        verbose_name_plural = "Avtomobillar"
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def get_display_price(self):
        return self.discounted_price or self.base_price


class CarSpecification(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='specifications', verbose_name="Avtomobil")
    name = models.CharField(max_length=100, verbose_name="Xususiyat nomi")
    value = models.CharField(max_length=200, verbose_name="Qiymat")
    unit = models.CharField(max_length=30, blank=True, verbose_name="O'lchov birligi")
    order = models.PositiveIntegerField(default=0, verbose_name="Tartib")

    class Meta:
        verbose_name = "Texnik xususiyat"
        verbose_name_plural = "Texnik xususiyatlar"
        ordering = ['order']

    def __str__(self):
        return f"{self.car.name} - {self.name}: {self.value}"


class CarColor(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='colors', verbose_name="Avtomobil")
    name = models.CharField(max_length=100, verbose_name="Rang nomi")
    hex_code = models.CharField(max_length=7, verbose_name="HEX kod", help_text="#RRGGBB formatda")
    image = models.ImageField(upload_to='car_colors/', blank=True, verbose_name="Rasm")
    price_addition = models.BigIntegerField(default=0, verbose_name="Qo'shimcha narx (so'm)")

    class Meta:
        verbose_name = "Rang"
        verbose_name_plural = "Ranglar"

    def __str__(self):
        return f"{self.car.name} - {self.name}"


class CarImage(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='gallery', verbose_name="Avtomobil")
    image = models.ImageField(upload_to='car_gallery/', verbose_name="Rasm")
    alt_text = models.CharField(max_length=200, blank=True, verbose_name="Alt matn")
    order = models.PositiveIntegerField(default=0, verbose_name="Tartib")

    class Meta:
        verbose_name = "Galereya rasmi"
        verbose_name_plural = "Galereya rasmlari"
        ordering = ['order']

    def __str__(self):
        return f"{self.car.name} - Rasm {self.order}"
