from rest_framework import serializers

from apps.feed.models import Feed
from apps.spitch.models import Spitch
from apps.ask.models import Ask
from apps.authentication.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "photo")

class AskSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Ask
        fields = ("id", "text", "user")

class SpitchSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    likes = serializers.IntegerField(source='likes.count')

    class Meta:
        model = Spitch
        fields = ("id", "spitch", "thumb", "photo", "created", "user", "likes")





class ContentSpitchSerializer(serializers.ModelSerializer):
    ask = AskSerializer()
    user = UserSerializer()
    likes = serializers.IntegerField(source='likes.count')
    is_liked = serializers.SerializerMethodField()

    def get_is_liked(self, obj):
        return obj.likes.filter(user=self.context['request'].user).exists()

    class Meta:
        model = Spitch
        fields = ("id", "spitch", "thumb", "created", "ask", "user", "likes", "is_liked", "spitch_transcoded")

class ContentAskSerializer(serializers.ModelSerializer):
    spitchs = serializers.SerializerMethodField()
    user = UserSerializer()
    total = serializers.IntegerField(source="spitchs.count")

    def get_spitchs(self, obj):
        return SpitchSerializer(obj.spitchs.all()[:4], many=True).data

    class Meta:
        model = Ask
        fields = ("id", "text", "spitchs", "user", "total", "created")


class FeedObjectRelatedField(serializers.RelatedField):
    def to_representation(self, value):
        if isinstance(value, Spitch):
            serializer = ContentSpitchSerializer(value, context=self.context)
        elif isinstance(value, Ask):
            serializer = ContentAskSerializer(value)
        else:
            raise Exception('Unexpected type of tagged object')

        return serializer.data


class FeedListSerializer(serializers.ModelSerializer):
    content_object = ContentSpitchSerializer(read_only=True)

    class Meta:
        model = Feed
        fields = ("id", "feed_type", "content_object")



class UpdateFeedSerializer(serializers.ModelSerializer):

    class Meta:
        model = Feed
        fields = ("id", "active", )