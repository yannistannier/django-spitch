# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


fieldsets = list(UserAdmin.fieldsets)
fieldsets[1][1]['fields'] = ('first_name', 'last_name', 'email', 'photo', 'type', 'idsn', 'fcm', 'title')

@admin.register(User)
class UserAdmin(UserAdmin):
    fieldsets = fieldsets
    list_display = ('username', 'email', 'is_staff', 'date_joined')

