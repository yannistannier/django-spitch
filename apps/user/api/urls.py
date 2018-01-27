# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.conf.urls import url
from .views import *
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register(r'^user', UserViewSet, base_name='user-viewset')


urlpatterns =  [
    url(r'^user/me/$', UserMeRetrieveApi.as_view(), name='user-me'),

    # url(r'^user/(?P<pk>\d+)/$', UserRetrieveApi.as_view(), name='user'),

    url(r'^user/(?P<pk>\d+)/spitch/$', SpitchUserList.as_view(), name='spitch'),
    url(r'^user/(?P<pk>\d+)/ask/$', AskUserList.as_view(), name='ask'),
    url(r'^user/search/$', SearchUserList.as_view(), name='search_user'),

    # url(r'^user/top/spitcher$', UserTopSpitcher.as_view(), name='user-top-spitcher'),
] + router.urls