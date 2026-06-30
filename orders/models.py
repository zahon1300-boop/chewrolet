from django.db import models


class TestDriveRequest(models.Model):
    STATUS_CHOICES = [
        ('new', 'Yangi'),
        ('confirmed', 'Tasdiqlangan'),
        ('completed', 'Bajarilgan'),
        ('cancelled', 'Bekor qilingan'),
    ]

    full_name = models.CharField(max_length=200, verbose_name="To'liq ism")
    phone = models.CharField(max_length=20, verbose_name="Telefon")
    email = models.EmailField(blank=True, verbose_name="Email")
    car = models.ForeignKey('cars.Car', on_delete=models.SET_NULL, null=True, verbose_name="Avtomobil")
    dealer = models.ForeignKey('dealers.Dealer', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Diler")
    preferred_date = models.DateField(null=True, blank=True, verbose_name="Afzal sana")
    message = models.TextField(blank=True, verbose_name="Izoh")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name="Holat")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Test drive so'rovi"
        verbose_name_plural = "Test drive so'rovlari"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.full_name} - {self.car} ({self.created_at.date()})"


class ContactRequest(models.Model):
    STATUS_CHOICES = [
        ('new', 'Yangi'),
        ('in_progress', 'Ko\'rib chiqilmoqda'),
        ('resolved', 'Hal qilindi'),
    ]
    full_name = models.CharField(max_length=200, verbose_name="To'liq ism")
    phone = models.CharField(max_length=20, verbose_name="Telefon")
    email = models.EmailField(blank=True, verbose_name="Email")
    subject = models.CharField(max_length=300, blank=True, verbose_name="Mavzu")
    message = models.TextField(verbose_name="Xabar")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name="Holat")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Murojaat"
        verbose_name_plural = "Murojaatlar"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.full_name} - {self.subject or 'Murojaat'}"


class CarOrder(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Kutilmoqda'),
        ('approved', 'Tasdiqlangan'),
        ('in_production', 'Ishlab chiqarilmoqda'),
        ('ready', 'Tayyor'),
        ('delivered', 'Yetkazilgan'),
        ('cancelled', 'Bekor qilingan'),
    ]
    PAYMENT_TYPE = [
        ('cash', 'Naqd'),
        ('credit', 'Kredit'),
        ('leasing', 'Lizing'),
    ]

    order_number = models.CharField(max_length=50, unique=True, verbose_name="Shartnoma raqami")
    full_name = models.CharField(max_length=200, verbose_name="To'liq ism")
    phone = models.CharField(max_length=20, verbose_name="Telefon")
    email = models.EmailField(blank=True, verbose_name="Email")
    passport = models.CharField(max_length=20, blank=True, verbose_name="Pasport seriyasi")
    
    car = models.ForeignKey('cars.Car', on_delete=models.SET_NULL, null=True, verbose_name="Avtomobil")
    color = models.ForeignKey('cars.CarColor', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Rang")
    dealer = models.ForeignKey('dealers.Dealer', on_delete=models.SET_NULL, null=True, verbose_name="Diler")
    
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPE, verbose_name="To'lov turi")
    total_price = models.BigIntegerField(verbose_name="Jami narx (so'm)")
    down_payment = models.BigIntegerField(null=True, blank=True, verbose_name="Boshlang'ich to'lov (so'm)")
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Holat")
    notes = models.TextField(blank=True, verbose_name="Izohlar")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Buyurtma"
        verbose_name_plural = "Buyurtmalar"
        ordering = ['-created_at']

    def __str__(self):
        return f"#{self.order_number} - {self.full_name} ({self.car})"
