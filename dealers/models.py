from django.db import models


class Region(models.Model):
    name = models.CharField(max_length=100, verbose_name="Viloyat nomi")
    slug = models.SlugField(unique=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Viloyat"
        verbose_name_plural = "Viloyatlar"
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class Dealer(models.Model):
    MARKET_TYPE = [
        ('local', 'Ichki bozor'),
        ('export', 'Tashqi bozor'),
        ('parts', 'Ehtiyot qismlar'),
        ('parts_export', 'Ehtiyot qismlar (tashqi bozor)'),
    ]

    name = models.CharField(max_length=200, verbose_name="Diler nomi")
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Viloyat")
    market_type = models.CharField(max_length=20, choices=MARKET_TYPE, default='local', verbose_name="Bozor turi")
    address = models.TextField(verbose_name="Manzil")
    phone = models.CharField(max_length=20, verbose_name="Telefon")
    phone2 = models.CharField(max_length=20, blank=True, verbose_name="Qo'shimcha telefon")
    email = models.EmailField(blank=True, verbose_name="Email")
    website = models.URLField(blank=True, verbose_name="Veb-sayt")
    
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, verbose_name="Kenglik")
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, verbose_name="Uzunlik")

    working_hours = models.CharField(max_length=100, blank=True, verbose_name="Ish vaqti")
    is_active = models.BooleanField(default=True, verbose_name="Faol")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Diler"
        verbose_name_plural = "Dilerlar"
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class ServiceCenter(models.Model):
    dealer = models.ForeignKey(Dealer, on_delete=models.CASCADE, related_name='service_centers', verbose_name="Diler")
    name = models.CharField(max_length=200, verbose_name="Servis markazi nomi")
    address = models.TextField(verbose_name="Manzil")
    phone = models.CharField(max_length=20, verbose_name="Telefon")
    is_active = models.BooleanField(default=True, verbose_name="Faol")

    class Meta:
        verbose_name = "Servis markazi"
        verbose_name_plural = "Servis markazlari"

    def __str__(self):
        return self.name
