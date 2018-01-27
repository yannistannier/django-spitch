# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.conf.urls import url

from .views import *

urlpatterns = [
    url(r'^notification/$', NotificationApiView.as_view(), name='notification'),
    url(r'^notification/count/$', CountNotificationApiView.as_view(), name='count-notification'),
]