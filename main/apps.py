"""
main ilovasining konfiguratsiyasi.
"""

from django.apps import AppConfig


class MainConfig(AppConfig):
    """Asosiy ilova konfiguratsiyasi."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "main"
    verbose_name = "Asosiy Ilova"

    def ready(self) -> None:
        """Ilova yuklangandan keyin signallarni ulash."""
        import main.signals  # noqa: F401
