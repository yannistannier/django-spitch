import re

from rest_framework import serializers
from ..models import Ask, Tag, Asktag
from apps.authentication.models import User
from apps.worker.tasks import ask

class AskCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ask
        fields = ('text',)
        extra_kwargs = { 'text': {"min_length" : 3} }

    def create(self, validated_data):
        instance = super(AskCreateSerializer, self).create(validated_data)
        hashtags = set(map(str.lower, re.findall(r"#(\w+)", validated_data['text'])))
        receivers = set(map(str.lower, re.findall(r"@(\w+)", validated_data['text'])))

        for hash in hashtags:
            tag, created = Tag.objects.get_or_create(tag=hash.lower())
            Asktag.objects.create(tag=tag, ask=instance)

        for receiver in receivers:
            if User.objects.filter(username__iexact=receiver).exists():
                to =  User.objects.get(username__iexact=receiver)
                if to != instance.user:
                    instance.receivers.add(to)

        #ask.delay(instance.id)

        return instance


class UserAskSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "photo")


class AskListSerializer(serializers.ModelSerializer):
    user = UserAskSerializer()
    spitchs = serializers.SerializerMethodField()

    def get_spitchs(self, obj):
        return obj.spitchs.filter(active=True).count()

    class Meta:
        model = Ask
        fields = ('text', 'id', 'user', 'created', 'spitchs')