# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.contrib import admin

from .models import Follow, FacebookFriend


@admin.register(FacebookFriend)
class FacebookFriendAdmin(admin.ModelAdmin):
    list_display = ('user', 'friend')


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'follow')

