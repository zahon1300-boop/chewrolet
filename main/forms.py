"""
main/forms.py — Loyiha formlari.

RegisterForm      — yangi foydalanuvchi ro'yxatdan o'tkazish
UserProfileForm   — foydalanuvchi profilini tahrirlash
UserUpdateForm    — asosiy ma'lumotlarni yangilash
"""

from __future__ import annotations

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from main.models import UserProfile

User = get_user_model()

# Qabul qilinadigan rasm formatlari
ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/webp"}
MAX_IMAGE_SIZE_MB = 5


# ==============================================================================
# RO'YXATDAN O'TISH FORMASI
# ==============================================================================

class RegisterForm(UserCreationForm):
    """
    Yangi foydalanuvchi ro'yxatdan o'tkazish formasi.

    Django UserCreationForm asosida qurilgan.
    Qo'shimcha: email, first_name, last_name maydonlari.
    """

    first_name = forms.CharField(
        max_length=150,
        required=True,
        label="Ism",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Ismingizni kiriting",
            "autofocus": True,
        }),
    )
    last_name = forms.CharField(
        max_length=150,
        required=True,
        label="Familiya",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Familiyangizni kiriting",
        }),
    )
    email = forms.EmailField(
        required=True,
        label="Elektron pochta",
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "example@email.com",
        }),
    )

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")
        widgets = {
            "username": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "foydalanuvchi_nomi",
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Password maydonlariga Bootstrap class qo'shish
        self.fields["password1"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Kamida 8 ta belgi",
        })
        self.fields["password2"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Parolni qayta kiriting",
        })
        self.fields["password1"].label = "Parol"
        self.fields["password2"].label = "Parolni tasdiqlang"
        self.fields["username"].label = "Foydalanuvchi nomi"
        self.fields["username"].help_text = (
            "150 ta belgigacha. Faqat harflar, raqamlar va @/./+/-/_ belgilari."
        )

    def clean_email(self) -> str:
        """Email takrorlanmasligini tekshiradi."""
        email = self.cleaned_data.get("email", "").strip().lower()
        if email and User.objects.filter(email=email).exists():
            raise ValidationError(
                "Bu elektron pochta manzili allaqachon ro'yxatdan o'tgan."
            )
        return email


# ==============================================================================
# FOYDALANUVCHI ASOSIY MA'LUMOTLARI
# ==============================================================================

class UserUpdateForm(forms.ModelForm):
    """Foydalanuvchi asosiy ma'lumotlarini tahrirlash."""

    first_name = forms.CharField(
        max_length=150,
        required=False,
        label="Ism",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Ismingizni kiriting",
        }),
    )
    last_name = forms.CharField(
        max_length=150,
        required=False,
        label="Familiya",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Familiyangizni kiriting",
        }),
    )
    email = forms.EmailField(
        required=False,
        label="Elektron pochta",
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "example@email.com",
        }),
    )

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")

    def clean_email(self) -> str:
        email = self.cleaned_data.get("email", "").strip().lower()
        if email:
            qs = User.objects.filter(email=email).exclude(pk=self.instance.pk)
            if qs.exists():
                raise ValidationError(
                    "Bu elektron pochta manzili allaqachon ro'yxatdan o'tgan."
                )
        return email


# ==============================================================================
# PROFIL FORMASI
# ==============================================================================

class UserProfileForm(forms.ModelForm):
    """Foydalanuvchi profil ma'lumotlarini tahrirlash."""

    class Meta:
        model = UserProfile
        fields = ("avatar", "bio", "phone", "address", "city", "date_of_birth")
        widgets = {
            "avatar": forms.FileInput(attrs={
                "class": "form-control",
                "accept": "image/jpeg,image/png,image/webp",
            }),
            "bio": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "O'zingiz haqingizda qisqacha yozing...",
                "maxlength": 500,
            }),
            "phone": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "+998901234567",
            }),
            "address": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Ko'cha, uy raqami",
            }),
            "city": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Shahar nomini kiriting",
            }),
            "date_of_birth": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date",
            }),
        }
        labels = {
            "avatar": "Profil rasmi",
            "bio": "O'zim haqimda",
            "phone": "Telefon raqami",
            "address": "Manzil",
            "city": "Shahar",
            "date_of_birth": "Tug'ilgan sana",
        }

    def clean_avatar(self):
        avatar = self.cleaned_data.get("avatar")
        if avatar:
            if avatar.size > MAX_IMAGE_SIZE_MB * 1024 * 1024:
                raise ValidationError(
                    f"Rasm hajmi {MAX_IMAGE_SIZE_MB} MB dan oshmasligi kerak."
                )
            if avatar.content_type not in ALLOWED_IMAGE_TYPES:
                raise ValidationError(
                    "Faqat JPEG, PNG va WebP formatdagi rasmlar qabul qilinadi."
                )
        return avatar
