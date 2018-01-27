from django.conf import settings
from django.db.models.signals import pre_delete, post_save
from django.dispatch import receiver
from apps.core.sync import SyncUser
from rest_framework.authtoken.models import Token


@receiver(pre_delete, sender=settings.AUTH_USER_MODEL)
def signal_pre_delete(sender, instance=None, **kwargs):
    SyncUser(instance.id).delete()


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

