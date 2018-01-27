# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import requests

from drf_extra_fields.fields import Base64ImageField
from django.core.files.base import ContentFile
from rest_framework import serializers

from ..models import User
from apps.worker.tasks import sync_user



# Refactor ---------------------------------------------------------------
# Refactor ---------------------------------------------------------------

class FacebookRegisterSerializer(serializers.ModelSerializer):
    email = serializers.CharField()
    photo = serializers.CharField(required=False, write_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'username', 'photo', 'idsn']
        extra_kwargs = {
            'first_name': {'required': False, 'write_only': True},
            'last_name': {'required': False, 'write_only': True},
            'username': {'write_only': True},
            'email': {'write_only': True},
            'idsn': {'write_only': True, 'required':True},
        }

    def create(self, validated_data):
        url = validated_data.get('photo')
        del validated_data['photo']
        user = User.objects.create_user(type="facebook", **validated_data)

        img = requests.get(url)

        if img.status_code == 200:
            url = url.split('/')[-1]
            filename = url[:url.find('?')] if '?' in url else url
            user.photo.save(filename, ContentFile(img.content), save=True)

        return user


class AuthFCMSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['fcm']
        extra_kwargs = {
            'fcm': {'required': True}
            }

# Refactor ---------------------------------------------------------------
# Refactor ---------------------------------------------------------------





# class AuthMeSerializer(serializers.ModelSerializer):
#     photo = Base64ImageField()
#
#     class Meta:
#         model = User
#         fields = ['email', 'first_name', 'last_name', 'username', 'photo', 'title']
#
#
#
# class UserRsRegisterSerializer(serializers.ModelSerializer):
#     LOGIN_TYPE={
#         'facebook' : 'facebook',
#         'twitter': 'twitter'
#
#     }
#     token = serializers.CharField(read_only=True)
#     photo = serializers.CharField(required=False, write_only=True)
#     type = serializers.ChoiceField(choices=LOGIN_TYPE, required=True, write_only=True)
#
#     class Meta:
#         model = User
#         fields = ['id', 'email', 'first_name', 'last_name', 'username', 'token', 'photo', 'type', 'idsn']
#         read_only_fields = ('token','id')
#         extra_kwargs = {
#             'first_name': {'required': False, 'write_only': True},
#             'last_name': {'required': False, 'write_only': True},
#             'username': {'write_only': True},
#             'email': {'write_only': True},
#             'idsn': {'write_only': True, 'required':True},
#         }
#
#     def create(self, validated_data):
#         url = validated_data.get('photo')
#         del validated_data['photo']
#         user = User.objects.create_user(**validated_data)
#
#         img = requests.get(url)
#
#         if img.status_code == 200:
#             url = url.split('/')[-1]
#             filename = url[:url.find('?')] if '?' in url else url
#             user.photo.save(filename, ContentFile(img.content), save=True)
#
#         return {'token' : user.get_token(), 'id' : user.id }
#
#
#
#
# class UserEmailRegisterSerializer(serializers.ModelSerializer):
#     token = serializers.CharField(read_only=True)
#
#     class Meta:
#         model = User
#         fields = ['id', 'email', 'password', 'first_name', 'last_name', 'username', 'token']
#         read_only_fields = ('token','id')
#         extra_kwargs = {
#             'password': {'write_only': True},
#             'first_name': {'required': False, 'write_only': True},
#             'last_name': {'required': False, 'write_only': True},
#             'username': {'write_only': True},
#             'email': {'write_only': True},
#         }
#
#     def create(self, validated_data):
#         user = User.objects.create_user(**validated_data)
#         sync_user.delay(user.id, "create")
#         return {'token' : user.get_token()}


