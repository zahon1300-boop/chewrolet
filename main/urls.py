"""
main/urls.py — Asosiy ilova URL marshrutlari.
"""

from django.urls import path
from main import views

app_name = "main"

urlpatterns = [
    # Asosiy sahifa
    path("", views.HomeView.as_view(), name="home"),

    # Ro'yxatdan o'tish
    path("register/", views.RegisterView.as_view(), name="register"),

    # Avtomobillar
    path("cars/", views.CarListView.as_view(), name="car_list"),
    path("cars/<slug:slug>/", views.CarDetailView.as_view(), name="car_detail"),

    # Yangiliklar
    path("news/", views.NewsListView.as_view(), name="news_list"),
    path("news/<slug:slug>/", views.NewsDetailView.as_view(), name="news_detail"),

    # Profil (himoyalangan)
    path("profile/", views.ProfileView.as_view(), name="profile"),

    # Qidiruv
    path("search/", views.SearchView.as_view(), name="search"),
]
