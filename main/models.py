"""
main/models.py — Chevrolet UZ loyihasining asosiy modellari.

Bu modul quyidagi modellarni o'z ichiga oladi:
- CarBrand: Avtomobil brendlari
- CarCategory: Avtomobil kategoriyalari
- Car: Asosiy avtomobil modeli (texnik xarakteristikalar bilan)
- CarImage: Ko'p rasmlar galereyasi (Car bilan bog'liq)
- News: Yangiliklar
- UserProfile: Foydalanuvchi profili (OneToOneField)
"""

from __future__ import annotations

import logging
import os
from decimal import Decimal
from typing import TYPE_CHECKING

from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from PIL import Image

if TYPE_CHECKING:
    pass

logger = logging.getLogger(__name__)
User = get_user_model()


# ==============================================================================
# YORDAMCHI FUNKSIYALAR
# ==============================================================================

def car_image_upload_path(instance: "CarImage", filename: str) -> str:
    """
    Avtomobil rasmlarini saqlash yo'lini dinamik yaratadi.
    Naqsh: media/cars/<car_slug>/<filename>
    """
    ext = filename.rsplit(".", 1)[-1].lower()
    safe_name = f"car_{instance.car.slug}_{instance.order}.{ext}"
    return os.path.join("cars", instance.car.slug, safe_name)


def news_image_upload_path(instance: "News", filename: str) -> str:
    """
    Yangilik rasmini saqlash yo'lini dinamik yaratadi.
    Naqsh: media/news/<year>/<month>/<filename>
    """
    ext = filename.rsplit(".", 1)[-1].lower()
    now = timezone.now()
    return os.path.join("news", str(now.year), str(now.month), f"news_{instance.pk or 'new'}.{ext}")


def avatar_upload_path(instance: "UserProfile", filename: str) -> str:
    """
    Foydalanuvchi avatari saqlash yo'li.
    Naqsh: media/avatars/<user_id>/<filename>
    """
    ext = filename.rsplit(".", 1)[-1].lower()
    return os.path.join("avatars", str(instance.user.pk), f"avatar.{ext}")


def optimize_image(
    image_path: str,
    max_width: int = 1920,
    max_height: int = 1080,
    quality: int = 85,
) -> None:
    """
    Rasmni optimallashtiradi: o'lchamini kamaytiradi va sifatni saqlaydi.

    Args:
        image_path: Rasm fayli yo'li
        max_width: Maksimal kenglik (piksel)
        max_height: Maksimal balandlik (piksel)
        quality: JPEG sifati (0–100)
    """
    try:
        with Image.open(image_path) as img:
            # EXIF ma'lumotlari asosida to'g'ri yo'nalish
            if hasattr(img, "_getexif") and img._getexif():
                exif = img._getexif()
                orientation_key = 274  # EXIF orientation tag
                if exif and orientation_key in exif:
                    orientation = exif[orientation_key]
                    rotations = {3: 180, 6: 270, 8: 90}
                    if orientation in rotations:
                        img = img.rotate(rotations[orientation], expand=True)

            # O'lchamni kamaytirish (nisbatni saqlagan holda)
            if img.width > max_width or img.height > max_height:
                img.thumbnail((max_width, max_height), Image.LANCZOS)

            # RGB formatiga o'tkazish (PNG, WebP kabi formatlar uchun)
            if img.mode in ("RGBA", "P", "LA"):
                background = Image.new("RGB", img.size, (255, 255, 255))
                if img.mode == "RGBA":
                    background.paste(img, mask=img.split()[3])
                else:
                    background.paste(img)
                img = background

            img.save(image_path, format="JPEG", quality=quality, optimize=True)
            logger.debug("Rasm optimallashtirildi: %s", image_path)

    except Exception as exc:
        logger.error("Rasmni optimallashtishda xato: %s — %s", image_path, exc)


# ==============================================================================
# BRAND VA KATEGORIYA
# ==============================================================================

class CarBrand(models.Model):
    """Avtomobil brendi modeli (Chevrolet, Cadillac va h.k.)."""

    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Brend nomi",
    )
    slug = models.SlugField(
        max_length=120,
        unique=True,
        verbose_name="Slug (URL)",
    )
    logo = models.ImageField(
        upload_to="brands/",
        blank=True,
        null=True,
        verbose_name="Brend logotipi",
    )
    description = models.TextField(
        blank=True,
        verbose_name="Tavsif",
    )

    class Meta:
        verbose_name = "Avtomobil brendi"
        verbose_name_plural = "Avtomobil brendlari"
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class CarCategory(models.Model):
    """Avtomobil kategoriyasi (Sedan, SUV, Crossover va h.k.)."""

    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Kategoriya nomi",
    )
    slug = models.SlugField(
        max_length=120,
        unique=True,
        verbose_name="Slug (URL)",
    )
    description = models.TextField(
        blank=True,
        verbose_name="Tavsif",
    )
    icon_class = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Bootstrap Icon klassi",
        help_text="Masalan: bi-car-front",
    )

    class Meta:
        verbose_name = "Kategoriya"
        verbose_name_plural = "Kategoriyalar"
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


# ==============================================================================
# AVTOMOBIL MODELI
# ==============================================================================

class Car(models.Model):
    """
    Asosiy avtomobil modeli.

    Texnik xarakteristikalar, narx, slug va multimedia ma'lumotlarini saqlaydi.
    """

    class TransmissionType(models.TextChoices):
        AUTOMATIC = "AT", "Avtomat"
        MANUAL = "MT", "Mexanik"
        CVT = "CVT", "Variator (CVT)"
        DSG = "DSG", "Robot (DSG)"

    class DriveType(models.TextChoices):
        FRONT = "FWD", "Old g'ildirak"
        REAR = "RWD", "Orqa g'ildirak"
        AWD = "AWD", "To'liq yurish (AWD)"
        FOUR_WD = "4WD", "4x4 (4WD)"

    class FuelType(models.TextChoices):
        PETROL = "petrol", "Benzin"
        DIESEL = "diesel", "Dizel"
        HYBRID = "hybrid", "Gibrid"
        ELECTRIC = "electric", "Elektr"
        GAS = "gas", "Gaz (LPG/CNG)"

    # --- Asosiy ma'lumotlar ---
    brand = models.ForeignKey(
        CarBrand,
        on_delete=models.PROTECT,
        related_name="cars",
        verbose_name="Brend",
    )
    category = models.ForeignKey(
        CarCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="cars",
        verbose_name="Kategoriya",
    )
    name = models.CharField(
        max_length=200,
        verbose_name="Mashina nomi",
        help_text="Masalan: Chevrolet Tracker 2024",
    )
    model_year = models.PositiveSmallIntegerField(
        verbose_name="Ishlab chiqarilgan yil",
        validators=[MinValueValidator(1900)],
    )
    slug = models.SlugField(
        max_length=250,
        unique=True,
        verbose_name="Slug (URL)",
        help_text="Avtomatik to'ldiriladi",
    )
    short_description = models.TextField(
        max_length=500,
        blank=True,
        verbose_name="Qisqa tavsif",
    )
    full_description = models.TextField(
        blank=True,
        verbose_name="To'liq tavsif",
    )

    # --- Narx ---
    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
        verbose_name="Narxi (USD)",
    )
    price_uzs = models.DecimalField(
        max_digits=15,
        decimal_places=0,
        null=True,
        blank=True,
        verbose_name="Narxi (UZS)",
    )
    is_price_negotiable = models.BooleanField(
        default=False,
        verbose_name="Narx kelishiladi",
    )

    # --- Dvigatel ---
    engine_volume = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        null=True,
        blank=True,
        verbose_name="Dvigatel hajmi (L)",
        help_text="Masalan: 1.5",
    )
    engine_power_hp = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        verbose_name="Quvvat (ot kuchi)",
    )
    engine_power_kw = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        verbose_name="Quvvat (kVt)",
    )
    engine_torque = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        verbose_name="Burovchi moment (Nm)",
    )
    fuel_type = models.CharField(
        max_length=10,
        choices=FuelType.choices,
        default=FuelType.PETROL,
        verbose_name="Yoqilg'i turi",
    )
    fuel_consumption_city = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        null=True,
        blank=True,
        verbose_name="Shahar sarfi (L/100km)",
    )
    fuel_consumption_highway = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        null=True,
        blank=True,
        verbose_name="Magistral sarfi (L/100km)",
    )

    # --- Uzatmalar qutisi ---
    transmission = models.CharField(
        max_length=5,
        choices=TransmissionType.choices,
        default=TransmissionType.AUTOMATIC,
        verbose_name="Uzatmalar qutisi",
    )
    gears_count = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        verbose_name="Pog'onalar soni",
    )
    drive_type = models.CharField(
        max_length=5,
        choices=DriveType.choices,
        default=DriveType.FRONT,
        verbose_name="Yurish turi",
    )

    # --- Tezlik va dinamika ---
    acceleration_0_100 = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        null=True,
        blank=True,
        verbose_name="0–100 km/s (soniya)",
    )
    max_speed = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        verbose_name="Maksimal tezlik (km/s)",
    )

    # --- O'lcham va og'irlik ---
    length_mm = models.PositiveIntegerField(
        null=True, blank=True, verbose_name="Uzunlik (mm)"
    )
    width_mm = models.PositiveIntegerField(
        null=True, blank=True, verbose_name="Kengligi (mm)"
    )
    height_mm = models.PositiveIntegerField(
        null=True, blank=True, verbose_name="Balandligi (mm)"
    )
    wheelbase_mm = models.PositiveIntegerField(
        null=True, blank=True, verbose_name="G'ildiraklar oralig'i (mm)"
    )
    curb_weight_kg = models.PositiveIntegerField(
        null=True, blank=True, verbose_name="Snaryad og'irligi (kg)"
    )
    trunk_volume_l = models.PositiveIntegerField(
        null=True, blank=True, verbose_name="Bagaj hajmi (litr)"
    )
    fuel_tank_l = models.PositiveIntegerField(
        null=True, blank=True, verbose_name="Yoqilg'i baki (litr)"
    )

    # --- Holat va ko'rinish ---
    color = models.CharField(
        max_length=100, blank=True, verbose_name="Rang"
    )
    is_active = models.BooleanField(
        default=True, verbose_name="Faol (saytda ko'rinsin)"
    )
    is_featured = models.BooleanField(
        default=False, verbose_name="Tavsiya etilgan (featured)"
    )
    is_new = models.BooleanField(
        default=True, verbose_name="Yangi model"
    )
    views_count = models.PositiveIntegerField(
        default=0, verbose_name="Ko'rishlar soni", editable=False
    )

    # --- Vaqt belgisi ---
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Yaratilgan vaqt"
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Yangilangan vaqt"
    )

    class Meta:
        verbose_name = "Avtomobil"
        verbose_name_plural = "Avtomobillar"
        ordering = ["-is_featured", "-created_at"]
        indexes = [
            models.Index(fields=["slug"]),
            models.Index(fields=["is_active", "is_featured"]),
            models.Index(fields=["brand", "category"]),
        ]

    def __str__(self) -> str:
        return f"{self.name} ({self.model_year})"

    def get_absolute_url(self) -> str:
        """Avtomobil sahifasiga URL qaytaradi."""
        return reverse("main:car_detail", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs) -> None:
        """Slug ni avtomatik generatsiya qiladi."""
        if not self.slug:
            base_slug = slugify(f"{self.name}-{self.model_year}")
            slug = base_slug
            counter = 1
            while Car.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    @property
    def main_image(self) -> "CarImage | None":
        """Asosiy (birinchi tartibdagi) rasmni qaytaradi."""
        return self.images.filter(is_main=True).first() or self.images.first()

    @property
    def price_formatted(self) -> str:
        """Narxni formatlangan ko'rinishda qaytaradi."""
        return f"${self.price:,.0f}"

    def increment_views(self) -> None:
        """Ko'rishlar sonini 1 ga oshiradi (F() bilan — race condition yo'q)."""
        from django.db.models import F
        Car.objects.filter(pk=self.pk).update(views_count=F("views_count") + 1)


# ==============================================================================
# AVTOMOBIL RASMLARI (Galereya)
# ==============================================================================

class CarImage(models.Model):
    """
    Avtomobil uchun galereya rasmlari.

    Har bir avtomobilga ko'p rasm qo'shish mumkin.
    is_main = True bo'lgan rasm asosiy thumbnail sifatida ishlatiladi.
    """

    car = models.ForeignKey(
        Car,
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name="Avtomobil",
    )
    image = models.ImageField(
        upload_to=car_image_upload_path,
        verbose_name="Rasm",
    )
    alt_text = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Alt matn (SEO uchun)",
    )
    caption = models.CharField(
        max_length=300,
        blank=True,
        verbose_name="Sarlavha",
    )
    is_main = models.BooleanField(
        default=False,
        verbose_name="Asosiy rasm",
    )
    order = models.PositiveSmallIntegerField(
        default=0,
        verbose_name="Tartib raqami",
    )
    uploaded_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Yuklangan vaqt",
    )

    class Meta:
        verbose_name = "Avtomobil rasmi"
        verbose_name_plural = "Avtomobil rasmlari"
        ordering = ["-is_main", "order", "uploaded_at"]

    def __str__(self) -> str:
        status = " (asosiy)" if self.is_main else ""
        return f"{self.car.name} rasmi #{self.order}{status}"

    def save(self, *args, **kwargs) -> None:
        """
        Rasmni saqlash va optimallashtirish.
        Agar is_main=True bo'lsa, boshqa rasmlarning is_main ni False ga o'tkazadi.
        """
        # Agar bu asosiy rasm bo'lsa, boshqalarni tozalash
        if self.is_main:
            CarImage.objects.filter(
                car=self.car, is_main=True
            ).exclude(pk=self.pk).update(is_main=False)

        # Alt text avtomatik to'ldirish
        if not self.alt_text:
            self.alt_text = f"{self.car.name} - rasm {self.order + 1}"

        super().save(*args, **kwargs)

        # Rasmni optimallashtirish
        if self.image and os.path.exists(self.image.path):
            optimize_image(
                self.image.path,
                max_width=1920,
                max_height=1080,
                quality=85,
            )


# ==============================================================================
# YANGILIKLAR
# ==============================================================================

class NewsCategory(models.Model):
    """Yangiliklar kategoriyasi."""

    name = models.CharField(max_length=100, unique=True, verbose_name="Nomi")
    slug = models.SlugField(max_length=120, unique=True)

    class Meta:
        verbose_name = "Yangilik kategoriyasi"
        verbose_name_plural = "Yangilik kategoriyalari"

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class News(models.Model):
    """
    Yangiliklar modeli.

    Avtomobil yangiliklari, aksiyalar va e'lonlar uchun ishlatiladi.
    """

    category = models.ForeignKey(
        NewsCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="news",
        verbose_name="Kategoriya",
    )
    title = models.CharField(
        max_length=300,
        verbose_name="Sarlavha",
    )
    slug = models.SlugField(
        max_length=320,
        unique=True,
        verbose_name="Slug (URL)",
    )
    excerpt = models.TextField(
        max_length=500,
        blank=True,
        verbose_name="Qisqacha mazmun",
    )
    content = models.TextField(
        verbose_name="To'liq matn",
    )
    cover_image = models.ImageField(
        upload_to=news_image_upload_path,
        blank=True,
        null=True,
        verbose_name="Muqova rasmi",
    )
    related_car = models.ForeignKey(
        Car,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="news",
        verbose_name="Bog'liq avtomobil",
    )
    is_published = models.BooleanField(
        default=False,
        verbose_name="Nashr etilgan",
    )
    is_featured = models.BooleanField(
        default=False,
        verbose_name="Muhim yangilik",
    )
    views_count = models.PositiveIntegerField(
        default=0,
        verbose_name="Ko'rishlar soni",
        editable=False,
    )
    published_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Nashr vaqti",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Yangilangan")

    class Meta:
        verbose_name = "Yangilik"
        verbose_name_plural = "Yangiliklar"
        ordering = ["-published_at", "-created_at"]
        indexes = [
            models.Index(fields=["slug"]),
            models.Index(fields=["is_published", "is_featured"]),
            models.Index(fields=["published_at"]),
        ]

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self) -> str:
        return reverse("main:news_detail", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs) -> None:
        """Slug va nashr vaqtini avtomatik boshqaradi."""
        if not self.slug:
            base_slug = slugify(self.title)[:300]
            slug = base_slug
            counter = 1
            while News.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug

        if self.is_published and not self.published_at:
            self.published_at = timezone.now()

        super().save(*args, **kwargs)

        # Muqova rasmini optimallashtirish
        if self.cover_image and os.path.exists(self.cover_image.path):
            optimize_image(
                self.cover_image.path,
                max_width=1200,
                max_height=675,
                quality=85,
            )

    def increment_views(self) -> None:
        """Ko'rishlar sonini oshiradi."""
        from django.db.models import F
        News.objects.filter(pk=self.pk).update(views_count=F("views_count") + 1)


# ==============================================================================
# FOYDALANUVCHI PROFILI
# ==============================================================================

class UserProfile(models.Model):
    """
    Foydalanuvchi profili.

    Django ichki User modeli bilan OneToOneField aloqasi mavjud.
    Avatar yuklanganda avtomatik optimallashtirish amalga oshiriladi.
    """

    phone_regex = RegexValidator(
        regex=r"^\+?1?\d{9,15}$",
        message="Telefon raqam to'g'ri formatda kiriting: '+998901234567'",
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
        verbose_name="Foydalanuvchi",
    )
    avatar = models.ImageField(
        upload_to=avatar_upload_path,
        blank=True,
        null=True,
        verbose_name="Profil rasmi",
    )
    bio = models.TextField(
        max_length=500,
        blank=True,
        verbose_name="O'zim haqimda",
    )
    phone = models.CharField(
        max_length=17,
        validators=[phone_regex],
        blank=True,
        verbose_name="Telefon raqami",
    )
    address = models.CharField(
        max_length=300,
        blank=True,
        verbose_name="Manzil",
    )
    city = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Shahar",
    )
    date_of_birth = models.DateField(
        null=True,
        blank=True,
        verbose_name="Tug'ilgan sana",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Yangilangan")

    class Meta:
        verbose_name = "Foydalanuvchi profili"
        verbose_name_plural = "Foydalanuvchi profillari"

    def __str__(self) -> str:
        return f"{self.user.get_full_name() or self.user.username} profili"

    def get_absolute_url(self) -> str:
        return reverse("main:profile")

    def save(self, *args, **kwargs) -> None:
        """
        Profilni saqlaydi va avatarni optimallashtiradi.

        Eski rasmni o'chirish va yangi rasmni 400x400 ga qisqartirish amalga oshiriladi.
        """
        # Eski avatarni o'chirish (agar yangi yuklangan bo'lsa)
        try:
            old_profile = UserProfile.objects.get(pk=self.pk)
            if old_profile.avatar and old_profile.avatar != self.avatar:
                if os.path.exists(old_profile.avatar.path):
                    os.remove(old_profile.avatar.path)
                    logger.info("Eski avatar o'chirildi: %s", old_profile.avatar.path)
        except UserProfile.DoesNotExist:
            pass

        super().save(*args, **kwargs)

        # Yangi avatarni optimallashtirish (kvadrat kesish)
        if self.avatar and os.path.exists(self.avatar.path):
            self._resize_avatar()

    def _resize_avatar(self) -> None:
        """Avatarni 400x400 o'lchamga qisqartiradi va markazdan kesib oladi."""
        try:
            with Image.open(self.avatar.path) as img:
                # Kvadrat kesish (crop to center)
                min_side = min(img.width, img.height)
                left = (img.width - min_side) // 2
                top = (img.height - min_side) // 2
                img = img.crop((left, top, left + min_side, top + min_side))

                # O'lchamni kamaytirish
                img = img.resize((400, 400), Image.LANCZOS)

                # RGB ga o'tkazish
                if img.mode != "RGB":
                    img = img.convert("RGB")

                img.save(self.avatar.path, format="JPEG", quality=90, optimize=True)
                logger.debug("Avatar optimallashtirildi: %s", self.avatar.path)

        except Exception as exc:
            logger.error("Avatarni optimallashtishda xato: %s", exc)

    @property
    def avatar_url(self) -> str:
        """Avatar URL ni qaytaradi yoki default rasm URL."""
        if self.avatar:
            return self.avatar.url
        return "/static/images/default-avatar.svg"


# ==============================================================================
# HERO BANNER MODELI
# ==============================================================================

def banner_image_upload_path(instance: "HeroBanner", filename: str) -> str:
    """Banner rasmini saqlash yo'li. media/banners/<filename>"""
    ext = filename.rsplit(".", 1)[-1].lower()
    import uuid
    safe_name = f"banner_{uuid.uuid4().hex[:8]}.{ext}"
    return os.path.join("banners", safe_name)


class HeroBanner(models.Model):
    """
    Bosh sahifadagi katta hero banner.

    Admin panel orqali rasm, sarlavha va tugma matni boshqariladi.
    Bir nechta banner bo'lishi mumkin — order maydoni bilan tartiblanadi.
    """

    title = models.CharField(
        max_length=200,
        verbose_name="Sarlavha",
        help_text="Katta banner ustidagi asosiy matn",
    )
    subtitle = models.CharField(
        max_length=300,
        blank=True,
        verbose_name="Kichik sarlavha",
    )
    image = models.ImageField(
        upload_to=banner_image_upload_path,
        verbose_name="Banner rasmi",
        help_text="Tavsiya etilgan o'lcham: 1920×900 px. JPEG yoki WebP formati.",
    )
    button_text = models.CharField(
        max_length=80,
        blank=True,
        default="Batafsil ko'rish",
        verbose_name="Tugma matni",
    )
    button_url = models.CharField(
        max_length=300,
        blank=True,
        default="/cars/",
        verbose_name="Tugma havolasi (URL)",
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Faol",
    )
    order = models.PositiveSmallIntegerField(
        default=0,
        verbose_name="Tartib raqami",
        help_text="Kichik son — birinchi ko'rsatiladi",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan")

    class Meta:
        verbose_name = "Hero Banner"
        verbose_name_plural = "Hero Bannerlar"
        ordering = ["order", "-created_at"]

    def __str__(self) -> str:
        return f"Banner: {self.title}"

    def save(self, *args, **kwargs) -> None:
        super().save(*args, **kwargs)
        # Bannerni optimallashtirish (1920x900)
        if self.image and os.path.exists(self.image.path):
            optimize_image(self.image.path, max_width=1920, max_height=900, quality=88)
