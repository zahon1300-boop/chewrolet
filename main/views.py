"""
main/views.py — Chevrolet UZ loyihasining asosiy ko'rinishlari.
"""

from __future__ import annotations

import logging
from typing import Any

from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, ListView, TemplateView

from main.forms import RegisterForm, UserProfileForm, UserUpdateForm
from main.models import Car, CarBrand, CarCategory, HeroBanner, News

logger = logging.getLogger(__name__)
User = get_user_model()


# ==============================================================================
# RO'YXATDAN O'TISH
# ==============================================================================

class RegisterView(View):
    """
    Yangi foydalanuvchi ro'yxatdan o'tkazish.
    GET  — forma ko'rsatish
    POST — formani qayta ishlash va foydalanuvchi yaratish
    """

    template_name = "registration/register.html"

    def get(self, request: HttpRequest) -> HttpResponse:
        if request.user.is_authenticated:
            return redirect("main:home")
        form = RegisterForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request: HttpRequest) -> HttpResponse:
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(
                request,
                f"🎉 Xush kelibsiz, {user.get_full_name() or user.username}! "
                "Ro'yxatdan muvaffaqiyatli o'tdingiz."
            )
            logger.info("Yangi foydalanuvchi ro'yxatdan o'tdi: %s", user.username)
            return redirect("main:home")

        messages.error(request, "❌ Formani to'g'ri to'ldiring.")
        return render(request, self.template_name, {"form": form})


# ==============================================================================
# ASOSIY SAHIFA
# ==============================================================================

class HomeView(TemplateView):
    """Asosiy sahifa — hero bannerlar, tavsiya etilgan avtomobillar, yangiliklar."""

    template_name = "main/index.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        # Hero bannerlar (admin orqali boshqariladi)
        context["hero_banners"] = HeroBanner.objects.filter(is_active=True).order_by("order")

        # Tavsiya etilgan avtomobillar
        context["featured_cars"] = (
            Car.objects.filter(is_active=True, is_featured=True)
            .select_related("brand", "category")
            .prefetch_related("images")
            .order_by("-created_at")[:6]
        )

        # Barcha aktiv avtomobillar
        context["latest_cars"] = (
            Car.objects.filter(is_active=True)
            .select_related("brand", "category")
            .prefetch_related("images")
            .order_by("-created_at")[:8]
        )

        # So'nggi nashr etilgan yangiliklar
        context["featured_news"] = (
            News.objects.filter(is_published=True, is_featured=True)
            .select_related("category")
            .order_by("-published_at")[:5]
        )
        context["latest_news"] = (
            News.objects.filter(is_published=True)
            .select_related("category")
            .order_by("-published_at")[:4]
        )

        context["categories"] = CarCategory.objects.all()
        context["brands"] = CarBrand.objects.all()[:8]
        return context


# ==============================================================================
# AVTOMOBILLAR RO'YXATI
# ==============================================================================

class CarListView(ListView):
    """Avtomobillar ro'yxati — filter va qidiruv bilan."""

    model = Car
    template_name = "main/car_list.html"
    context_object_name = "cars"
    paginate_by = 12

    def get_queryset(self) -> QuerySet[Car]:
        qs = (
            Car.objects.filter(is_active=True)
            .select_related("brand", "category")
            .prefetch_related("images")
        )

        brand_slug = self.request.GET.get("brand")
        if brand_slug:
            qs = qs.filter(brand__slug=brand_slug)

        category_slug = self.request.GET.get("category")
        if category_slug:
            qs = qs.filter(category__slug=category_slug)

        transmission = self.request.GET.get("transmission")
        if transmission:
            qs = qs.filter(transmission=transmission)

        fuel_type = self.request.GET.get("fuel_type")
        if fuel_type:
            qs = qs.filter(fuel_type=fuel_type)

        min_price = self.request.GET.get("min_price")
        max_price = self.request.GET.get("max_price")
        if min_price:
            try:
                qs = qs.filter(price__gte=float(min_price))
            except ValueError:
                pass
        if max_price:
            try:
                qs = qs.filter(price__lte=float(max_price))
            except ValueError:
                pass

        query = self.request.GET.get("q", "").strip()
        if query:
            qs = qs.filter(
                Q(name__icontains=query)
                | Q(short_description__icontains=query)
                | Q(brand__name__icontains=query)
            )

        valid_sorts = {
            "price_asc": "price",
            "price_desc": "-price",
            "newest": "-created_at",
            "oldest": "created_at",
            "popular": "-views_count",
            "featured": "-is_featured",
        }
        sort = self.request.GET.get("sort", "featured")
        return qs.order_by(valid_sorts.get(sort, "-is_featured"))

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["brands"] = CarBrand.objects.all()
        context["categories"] = CarCategory.objects.all()
        context["transmission_choices"] = Car.TransmissionType.choices
        context["fuel_choices"] = Car.FuelType.choices
        context["current_filters"] = {
            "brand": self.request.GET.get("brand", ""),
            "category": self.request.GET.get("category", ""),
            "transmission": self.request.GET.get("transmission", ""),
            "fuel_type": self.request.GET.get("fuel_type", ""),
            "min_price": self.request.GET.get("min_price", ""),
            "max_price": self.request.GET.get("max_price", ""),
            "q": self.request.GET.get("q", ""),
            "sort": self.request.GET.get("sort", ""),
        }
        return context


# ==============================================================================
# AVTOMOBIL BATAFSIL
# ==============================================================================

class CarDetailView(DetailView):
    """Bitta avtomobil batafsil sahifasi."""

    model = Car
    template_name = "main/car_detail.html"
    context_object_name = "car"

    def get_queryset(self) -> QuerySet[Car]:
        return (
            Car.objects.filter(is_active=True)
            .select_related("brand", "category")
            .prefetch_related("images", "news")
        )

    def get_object(self, queryset=None) -> Car:
        obj = super().get_object(queryset)
        obj.increment_views()
        return obj

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        car = self.object
        context["related_cars"] = (
            Car.objects.filter(is_active=True, category=car.category)
            .exclude(pk=car.pk)
            .select_related("brand")
            .prefetch_related("images")[:4]
        )
        context["gallery_images"] = car.images.order_by("-is_main", "order")
        return context


# ==============================================================================
# YANGILIKLAR
# ==============================================================================

class NewsListView(ListView):
    model = News
    template_name = "main/news_list.html"
    context_object_name = "news_list"
    paginate_by = 9

    def get_queryset(self) -> QuerySet[News]:
        qs = (
            News.objects.filter(is_published=True)
            .select_related("category", "related_car")
            .order_by("-published_at")
        )
        category_slug = self.request.GET.get("category")
        if category_slug:
            qs = qs.filter(category__slug=category_slug)
        query = self.request.GET.get("q", "").strip()
        if query:
            qs = qs.filter(Q(title__icontains=query) | Q(excerpt__icontains=query))
        return qs

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        from main.models import NewsCategory
        context["news_categories"] = NewsCategory.objects.all()
        context["current_category"] = self.request.GET.get("category", "")
        context["query"] = self.request.GET.get("q", "")
        return context


class NewsDetailView(DetailView):
    model = News
    template_name = "main/news_detail.html"
    context_object_name = "news"

    def get_queryset(self) -> QuerySet[News]:
        return News.objects.filter(is_published=True).select_related("category", "related_car")

    def get_object(self, queryset=None) -> News:
        obj = super().get_object(queryset)
        obj.increment_views()
        return obj

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["recent_news"] = (
            News.objects.filter(is_published=True)
            .exclude(pk=self.object.pk)
            .order_by("-published_at")[:4]
        )
        return context


# ==============================================================================
# PROFIL (LoginRequired)
# ==============================================================================

class ProfileView(LoginRequiredMixin, View):
    """Foydalanuvchi profil sahifasi — kirish talab qilinadi."""

    template_name = "main/profile.html"
    login_url = reverse_lazy("login")

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = UserProfileForm(instance=request.user.profile)
        return self._render(request, user_form, profile_form)

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        user_form = UserUpdateForm(data=request.POST, instance=request.user)
        profile_form = UserProfileForm(
            data=request.POST, files=request.FILES, instance=request.user.profile
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "✅ Profil muvaffaqiyatli yangilandi!")
            return redirect("main:profile")
        messages.error(request, "❌ Ma'lumotlarni to'g'ri kiriting.")
        return self._render(request, user_form, profile_form)

    def _render(self, request, user_form, profile_form) -> HttpResponse:
        return render(request, self.template_name, {
            "user_form": user_form,
            "profile_form": profile_form,
            "user": request.user,
            "profile": request.user.profile,
        })


# ==============================================================================
# QIDIRUV
# ==============================================================================

class SearchView(ListView):
    template_name = "main/search_results.html"
    context_object_name = "cars"
    paginate_by = 12

    def get_queryset(self) -> QuerySet[Car]:
        query = self.request.GET.get("q", "").strip()
        if not query:
            return Car.objects.none()
        return (
            Car.objects.filter(is_active=True)
            .filter(
                Q(name__icontains=query)
                | Q(short_description__icontains=query)
                | Q(brand__name__icontains=query)
            )
            .select_related("brand")
            .prefetch_related("images")
            .distinct()
        )

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get("q", "").strip()
        context["query"] = query
        if query:
            context["news_results"] = (
                News.objects.filter(is_published=True, title__icontains=query)
                .order_by("-published_at")[:5]
            )
        return context
