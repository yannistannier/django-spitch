from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .mixins import AuthMeMixin
from ..models import User
from apps.relation.models import FacebookFriend
from apps.authentication.facebook import Facebook
from apps.worker.tasks import sync_user, new_user
from apps.user.api.serializers import UserMeSerializer
from .serializers import FacebookRegisterSerializer, AuthFCMSerializer


class AuthFacebookView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        if "token" in request.data:
            fb = Facebook(request.data['token'])
            user = get_object_or_404(User, idsn=fb.get_id())

            if user.type == "facebook":
                token = user.token()
                user = UserMeSerializer(instance=user).data
                return Response({"token": token, "user": user}, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)



class AuthEmailUsernameCheckApiView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        if 'email' in request.data:
            if request.data['email']:
                if not User.objects.filter(email=request.data['email']).exists():
                    return Response(status=status.HTTP_200_OK)
        if 'username' in request.data:
            if request.data['username']:
                if not User.objects.filter(username__iexact=request.data['username']).exists():
                    return Response(status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)



class FacebookRegisterApiView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, format=None):

        if "token" in request.data and "username" in request.data:
            facebook = Facebook(request.data['token'])

            # User.objects.filter(idsn=facebook.get_id()).delete()

            serializer = FacebookRegisterSerializer(data=facebook.get_profile(request.data['username']))
            serializer.is_valid(raise_exception=True)
            serializer.save()

            user = UserMeSerializer(instance=serializer.instance)
            token = serializer.instance.token()

            friends_id = facebook.get_friends()

            if friends_id:
                friends = User.objects.filter(idsn__in=friends_id)
                FacebookFriend.objects.bulk_create(
                    [FacebookFriend(user_id=serializer.instance.id, friend=x) for x in friends.all()]
                    +
                    [FacebookFriend(user=x, friend_id=serializer.instance.id) for x in friends.all()]
                )

            sync_user.delay(serializer.data.get('id'), "create")

            #remove when betatest is over
            # new_user.delay(serializer.instance.id)

            return Response({"token": token, "user": user.data}, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)



class AuthFCMTokenApiView(AuthMeMixin, generics.UpdateAPIView):
    serializer_class = AuthFCMSerializer


# Refactor ---------------------------------------------------------------
# Refactor ---------------------------------------------------------------




# class AuthMeApiView(AuthMeMixin, generics.UpdateAPIView):
#     serializer_class = AuthMeSerializer
#
#     def update(self, request, *args, **kwargs):
#         super(AuthMeApiView, self).update(request, *args, **kwargs)
#         sync_user.delay(self.request.user.id, "update")
#         return Response({'token' : self.request.user.get_token()}, status=status.HTTP_200_OK)



# class AuthFacebookView(APIView):
#     permission_classes = (AllowAny,)
#
#     def post(self, request, format=None):
#         if "token" in request.data:
#             fb = Facebook(request.data['token'])
#             user = get_object_or_404(User, idsn=fb.get_id())
#             if user.type == "facebook":
#                 return Response({"token": user.get_token()}, status=status.HTTP_200_OK)
#         return Response(status=status.HTTP_400_BAD_REQUEST)


# class AuthRegisterApiView(generics.CreateAPIView):
#     serializer_class = UserEmailRegisterSerializer
#     permission_classes = (AllowAny,)


# class AuthFacebookRegisterApiView(APIView):
#     permission_classes = (AllowAny,)
#
#     def post(self, request, format=None):
#
#         if "token" in request.data and "username" in request.data:
#             facebook = Facebook(request.data['token'])
#
#             serializer = UserRsRegisterSerializer(data=facebook.get_profile(request.data['username']))
#             serializer.is_valid(raise_exception=True)
#             serializer.save()
#
#             friends_id = facebook.get_friends()
#
#             if friends_id:
#                 friends = User.objects.filter(idsn__in=friends_id)
#                 FacebookFriend.objects.bulk_create(
#                     [FacebookFriend(user_id=serializer.data.get('id'), friend=x) for x in friends.all()]
#                     +
#                     [FacebookFriend(user=x, friend_id=serializer.data.get('id')) for x in friends.all()]
#                 )
#
#             sync_user.delay(serializer.data.get('id'), "create")
#             return Response({'token' :  serializer.data.get('token') }, status=status.HTTP_200_OK)
#
#         return Response(status=status.HTTP_400_BAD_REQUEST)


# class AuthEmailUsernameCheckApiView(APIView):
#     permission_classes = (AllowAny,)
#
#     def post(self, request):
#         if 'email' in request.data:
#             if request.data['email']:
#                 if not User.objects.filter(email=request.data['email']).exists():
#                     return Response(status=status.HTTP_200_OK)
#         if 'username' in request.data:
#             if request.data['username']:
#                 if not User.objects.filter(username=request.data['username']).exists():
#                     return Response(status=status.HTTP_200_OK)
#
#         return Response(status=status.HTTP_401_UNAUTHORIZED)

#
# class AuthGeneratePresignedUrl(APIView): #type = photo ou video
#
#     def post(self, request):
#         if 'type' in request.data:
#             if request.data['type'] in ("video", "photo"):
#                 s3 = boto3.client('s3')
#                 key = settings.MEDIAFILES_LOCATION+"/"+str(request.user.id)+"/"+request.data['type']+"/test.jpg"
#                 post = s3.generate_presigned_post(
#                     Bucket=settings.AWS_STORAGE_BUCKET_NAME,
#                     Key=key,
#                     ExpiresIn=600
#                 )
#                 return Response(post, status=status.HTTP_200_OK)
#
#         return Response(status=status.HTTP_401_UNAUTHORIZED)
