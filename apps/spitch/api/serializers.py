from rest_framework import serializers
from ..models import Spitch, Report
from apps.authentication.models import User
from apps.ask.models import Ask



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
    ask = AskSerializer()
    likes = serializers.IntegerField(source='likes.count')
    is_liked = serializers.SerializerMethodField()

    def get_is_liked(self, obj):
        return obj.likes.filter(user=self.context['request'].user).exists()

    class Meta:
        model = Spitch
        fields = ("id", "user", "ask", "thumb", "spitch", "spitch_transcoded", "created", "likes", "is_liked")



class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ("spitch", )


class UpdateSpitchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Spitch
        fields = ("active", )
