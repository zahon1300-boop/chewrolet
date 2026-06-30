from django.db import models


class NewsCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name="Kategoriya")
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = "Yangilik kategoriyasi"
        verbose_name_plural = "Yangilik kategoriyalari"

    def __str__(self):
        return self.name


class News(models.Model):
    title = models.CharField(max_length=300, verbose_name="Sarlavha")
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(NewsCategory, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Kategoriya")
    content = models.TextField(verbose_name="Mazmun")
    image = models.ImageField(upload_to='news/', blank=True, verbose_name="Rasm")
    image_mobile = models.ImageField(upload_to='news/mobile/', blank=True, verbose_name="Mobil rasm")
    
    url_path = models.CharField(max_length=200, blank=True, verbose_name="URL yo'li")
    is_published = models.BooleanField(default=False, verbose_name="Nashr etilgan")
    is_slider = models.BooleanField(default=False, verbose_name="Slider'da ko'rsatish")
    slider_order = models.PositiveIntegerField(default=0, verbose_name="Slider tartibi")

    published_at = models.DateTimeField(null=True, blank=True, verbose_name="Nashr sanasi")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Yangilik"
        verbose_name_plural = "Yangiliklar"
        ordering = ['-published_at']

    def __str__(self):
        return self.title


class SpecialOffer(models.Model):
    title = models.CharField(max_length=300, verbose_name="Aksiya nomi")
    car = models.ForeignKey('cars.Car', on_delete=models.SET_NULL, null=True, blank=True, 
                            related_name='offers', verbose_name="Avtomobil")
    bank_name = models.CharField(max_length=100, blank=True, verbose_name="Bank nomi")
    description = models.TextField(verbose_name="Tavsif")
    image = models.ImageField(upload_to='offers/', blank=True, verbose_name="Rasm")
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, 
                                        verbose_name="Foiz stavkasi (%)")
    min_down_payment = models.PositiveIntegerField(null=True, blank=True, verbose_name="Minimal boshlang'ich to'lov (%)")
    max_months = models.PositiveIntegerField(null=True, blank=True, verbose_name="Maksimal muddat (oy)")
    
    is_active = models.BooleanField(default=True, verbose_name="Faol")
    valid_until = models.DateField(null=True, blank=True, verbose_name="Amal qilish muddati")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Maxsus taklif"
        verbose_name_plural = "Maxsus takliflar"
        ordering = ['-created_at']

    def __str__(self):
        return self.title
