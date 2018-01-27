from rest_framework import serializers
from apps.relation.models import Follow


class ItemNotificationSerializer(serializers.Serializer):
    type = serializers.IntegerField()
    user = serializers.DictField(default=None)
    obj = serializers.DictField(default=None)
    timestamp = serializers.IntegerField()
    vue = serializers.IntegerField(default=0)
    follow = serializers.SerializerMethodField()

    def get_follow(self, obj):
        if obj['type'] == 1 or obj['type'] == 4 :
            return Follow.objects.filter(user_id=self.context['user'], follow_id=obj['user']['id']).exists()
        return None

class NotificationSerializer(serializers.Serializer):
    items = ItemNotificationSerializer(many=True)
    next = serializers.CharField(default=None)
