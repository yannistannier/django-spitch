# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

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

    welcome = models.BooleanField(default=True)


    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')


    def token(self):
        return self.auth_token.key

