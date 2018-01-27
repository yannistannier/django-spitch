from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField
from apps.authentication.models import User
from apps.ask.models import Ask
from apps.spitch.models import Spitch


class UserMeSerializer(serializers.ModelSerializer):
    photo = Base64ImageField(required=False)

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'username', 'photo', 'title' ]
        read_only_fields = ('id',)




class UserSerializer(serializers.ModelSerializer):
    follow = serializers.SerializerMethodField()

    def get_follow(self, obj):
        return obj.followers.filter(user=self.context['request'].user).exists()

    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name", "photo", "title", "follow" )



class UserDatasSerializer(serializers.ModelSerializer):
    videos = serializers.SerializerMethodField()
    follows = serializers.SerializerMethodField()
    followers = serializers.SerializerMethodField()

    def get_videos(self, obj):
        return obj.spitchs.filter(active=True).count()

    def get_follows(self, obj):
        return obj.follows.count()

    def get_followers(self, obj):
        return obj.followers.count()


    class Meta:
        model = User
        fields = ("videos", "follows", "followers")




class UserAskSerializer(serializers.ModelSerializer):
    spitchs = serializers.SerializerMethodField()

    def get_spitchs(self, obj):
        return obj.spitchs.filter(active=True).count()

    class Meta:
        model = Ask
        fields = ("id", "text", "created", "spitchs")



class UserSpitchSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "photo")

class SpitchSerializer(serializers.ModelSerializer):
    ask = UserAskSerializer()
    user = UserSpitchSerializer()
    likes = serializers.IntegerField(source='likes.count')
    is_liked = serializers.SerializerMethodField()

    def get_is_liked(self, obj):
        return obj.likes.filter(user=self.context['request'].user).exists()

    class Meta:
        model = Spitch
        fields = ("id", "thumb", "video", "ask", "user", "likes", "is_liked", "spitch", "spitch_transcoded")



class SearchUserSerializer(serializers.ModelSerializer):
    follow = serializers.SerializerMethodField()

    def get_follow(self, obj):
        return obj.followers.filter(user=self.context['request'].user).exists()

    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name", "photo", "follow")

