"""
main/signals.py — Django signallari.

Foydalanuvchi yaratilganda avtomatik UserProfile ochadi.
"""

import logging

from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from main.models import UserProfile

logger = logging.getLogger(__name__)
User = get_user_model()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance: User, created: bool, **kwargs) -> None:  # type: ignore[type-arg]
    """
    Yangi foydalanuvchi yaratilganda avtomatik UserProfile ochadi.

    Args:
        sender: Signal yuboruvchi model (User)
        instance: Yangi yaratilgan User ob'ekti
        created: True — yangi yaratildi, False — yangilandi
    """
    if created:
        UserProfile.objects.get_or_create(user=instance)
        logger.info("Yangi profil yaratildi: %s", instance.username)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance: User, **kwargs) -> None:  # type: ignore[type-arg]
    """Foydalanuvchi yangilanganda profilni ham saqlaydi."""
    if hasattr(instance, "profile"):
        instance.profile.save()
