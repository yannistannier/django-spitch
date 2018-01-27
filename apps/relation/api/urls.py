# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.conf.urls import url
from .views import *

urlpatterns = [
    # url(r'^relation/generate-facebook-list/$', GenerateListFacebook.as_view(), name='relation-generate-facebook'),

    url(r'^relation/facebook-list/$', FacebookFriendListApiView.as_view(), name='relation-facebook'),
    url(r'^relation/follow/$', FollowCreateApiView.as_view(), name='follow'),
    url(r'^relation/unfollow/(?P<pk>\d+)/$', UnFollowDeleteApiView.as_view(), name='unfollow'),
    url(r'^relation/follow/all/$', FollowAllCreateApiView.as_view(), name='follow-all'),

    url(r'^relation/(?P<pk>\d+)/follows/$', ListFollowApiView.as_view(), name='follow-list'),
    url(r'^relation/(?P<pk>\d+)/followers/$', ListFollowerApiView.as_view(), name='follower-list'),
]