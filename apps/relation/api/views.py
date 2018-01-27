from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from .serializers import *
from apps.core.api.mixins import ContextMixin
from ..models import Follow, FacebookFriend
from apps.authentication.models import User
from apps.authentication.facebook import Facebook
from apps.worker.tasks import follow_user, follow_all



class ListFollowApiView(ContextMixin, generics.ListAPIView):
    serializer_class = ListFollowSerializer
    search_fields = ('follow__username', 'follow__first_name', 'follow__last_name')
    filter_backends = ( SearchFilter,)

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Follow.objects.filter(user=pk)


class ListFollowerApiView(ContextMixin, generics.ListAPIView):
    serializer_class = ListFollowerSerializer
    search_fields = ('user__username', 'user__first_name', 'user__last_name')
    filter_backends = (SearchFilter,)

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Follow.objects.filter(follow=pk)



class FacebookFriendListApiView(generics.ListAPIView):
    serializer_class = ListFacebookFriendSerializer

    def get_queryset(self):
        return FacebookFriend.objects.filter(user = self.request.user)



class FollowCreateApiView(generics.CreateAPIView):
    serializer_class = FollowSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        follow_user.delay(self.request.user.id, serializer.data['follow'])


class FollowAllCreateApiView(APIView):

    def post(self, request, format=None):
        follow_all.delay(self.request.user.id)
        return Response(status=status.HTTP_200_OK)


class UnFollowDeleteApiView(generics.DestroyAPIView):

    def get_object(self):
        return Follow.objects.filter(user_id=self.request.user.id, follow_id = self.kwargs['pk'])




# ---------------------------------------------

# class GenerateListFacebook(APIView):
#
#     def post(self, request, format=None):
#         serializer = GenerateFacebookList(data=request.data)
#         serializer.is_valid(raise_exception=True)
#
#         facebook = Facebook(serializer.validated_data['token'])
#
#         friends_id = facebook.get_friends()
#
#         if friends_id:
#             friends = User.objects.filter(idsn__in=friends_id)
#
#             FacebookFriend.objects.bulk_create(
#                 [FacebookFriend(user=self.request.user, friend=x) for x in friends.all()]
#                 +
#                 [FacebookFriend(user=x, friend=self.request.user) for x in friends.all()]
#             )
#
#         return Response({'token' : self.request.user.get_token()}, status=status.HTTP_200_OK)


