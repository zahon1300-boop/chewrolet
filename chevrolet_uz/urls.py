"""
Chevrolet UZ — asosiy URL sozlamalari.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView

urlpatterns = [
    # Admin panel
    path("admin", RedirectView.as_view(url="/admin/"), name="admin-redirect"),
    path("admin/", admin.site.urls),

    # Autentifikatsiya (login, logout, password reset)
    path("", include("django.contrib.auth.urls")),

    # Asosiy ilova
    path("", include("main.urls", namespace="main")),
]

# Media fayllarni ishlab chiqishda serve qilish
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Admin panel sarlavhasini sozlash
admin.site.site_header = "Chevrolet UZ — Boshqaruv Paneli"
admin.site.site_title = "Chevrolet UZ Admin"
admin.site.index_title = "Xush kelibsiz, Chevrolet UZ Admin!"
