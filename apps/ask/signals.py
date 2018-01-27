from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .models import Ask
from apps.core.sync import SyncAsk


@receiver(post_save, sender=Ask)
def signal_post_save(sender, instance=None, created=False, **kwargs):
    if not created:
        if instance.active is False:
            SyncAsk(instance.id).delete()


@receiver(pre_delete, sender=Ask)
def signal_pre_delete(sender, instance=None, **kwargs):
    SyncAsk(instance.id).delete()
