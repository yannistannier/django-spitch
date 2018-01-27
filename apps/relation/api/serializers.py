# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from rest_framework import serializers
from ..models import FacebookFriend, Follow
from apps.authentication.models import User


class ListFacebookFriendSerializer(serializers.ModelSerializer):

    id = serializers.StringRelatedField(source='friend.id')
    username = serializers.StringRelatedField(source='friend.username')
    first_name = serializers.StringRelatedField(source='friend.first_name')
    last_name = serializers.StringRelatedField(source='friend.last_name')
    photo = serializers.StringRelatedField(source='friend.photo.url')
    follow = serializers.SerializerMethodField()

    def get_follow(self, obj):
        return obj.user.follows.filter(follow=obj.friend).exists()
        # return Follow.objects.filter(user=obj.user, follow=obj.follow).exists()

    class Meta:
        model = FacebookFriend
        fields = ('id', 'username', 'first_name', 'last_name', 'photo', 'follow')



class FollowSerializer(serializers.ModelSerializer):

    class Meta:
        model = Follow
        fields = ('follow', )


class GenerateFacebookList(serializers.Serializer):
    token = serializers.CharField(required=True)



class ListFollowFollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ('id', 'username', 'first_name', 'last_name', 'photo')



class ListFollowSerializer(ListFollowFollowerSerializer):
    id = serializers.StringRelatedField(source='follow.id')
    username = serializers.StringRelatedField(source='follow.username')
    first_name = serializers.StringRelatedField(source='follow.first_name')
    last_name = serializers.StringRelatedField(source='follow.last_name')
    photo = serializers.StringRelatedField(source='follow.photo.url')
    follow = serializers.SerializerMethodField()

    def get_follow(self, obj):
        return obj.follow.followers.filter(user=self.context['request'].user).exists()

    class Meta:
        model = Follow
        fields = ('id', 'username', 'first_name', 'last_name', 'photo', 'follow')


class ListFollowerSerializer(ListFollowFollowerSerializer):
    id = serializers.StringRelatedField(source='user.id')
    username = serializers.StringRelatedField(source='user.username')
    first_name = serializers.StringRelatedField(source='user.first_name')
    last_name = serializers.StringRelatedField(source='user.last_name')
    photo = serializers.StringRelatedField(source='user.photo.url')
    follow = serializers.SerializerMethodField()

    def get_follow(self, obj):
        return obj.user.followers.filter(user=self.context['request'].user).exists()

    class Meta:
        model = Follow
        fields = ('id', 'username', 'first_name', 'last_name', 'photo', 'follow')