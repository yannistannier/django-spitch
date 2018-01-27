from django.conf import settings
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from apps.core.sync import SyncUser


@receiver(pre_delete, sender=settings.AUTH_USER_MODEL)
def signal_pre_delete(sender, instance=None, **kwargs):
    SyncUser(instance.id).delete()

