# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from rest_framework_jwt.settings import api_settings

from apps.core.fields import ImageField


@python_2_unicode_compatible
class User(AbstractUser):
    DEFAULT_PHOTO = 'default/default.jpg'

    email = models.EmailField(_('email address'), unique=True)
    photo = ImageField(_('photo'), blank=True, default=DEFAULT_PHOTO)
    fcm = models.CharField(max_length=250, null=True, blank=True) #FCM token for push notification
    type = models.CharField(default="email", max_length=10)
    idsn = models.CharField(max_length=128, null=True, db_index=True, blank=True) #ID facebook or twitter
    title = models.CharField(max_length=250, null=True, blank=True)

    lang = models.CharField(default="fr", max_length=10)
    country = models.CharField(default="FR", max_length=10)


    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')


    def get_token(self):
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(self)
        return jwt_encode_handler(payload)

