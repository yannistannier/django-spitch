from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from apps.authentication.models import User


class Feed(models.Model):

    FEED_TYPE = (
        (1, 'Spitch'),
        (2, 'Ask'),
    )

    user = models.ForeignKey(User)
    feed_type = models.PositiveIntegerField(choices=FEED_TYPE)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    active = models.BooleanField(default=True, db_index=True)
    created = models.DateTimeField(auto_now_add=True)


