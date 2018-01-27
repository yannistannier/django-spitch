from django.conf.urls import url

from .views import *

urlpatterns = [
    # url(r'^auth/me/$', AuthMeApiView.as_view(), name='update-user'),
    # url(r'^auth/token-auth/$', obtain_jwt_token),
    # url(r'^auth/facebook/$', AuthFacebookView.as_view()),
    #
    # url(r'^auth/register/$', AuthRegisterApiView.as_view(), name='register-user'),
    # url(r'^auth/register/facebook/$', AuthFacebookRegisterApiView.as_view(), name='register-user-rs'),
    #
    # url(r'^auth/presigned-url/$', AuthGeneratePresignedUrl.as_view(), name='presignated-url'),
    # url(r'^auth/check/$', AuthEmailUsernameCheckApiView.as_view(), name='checkrun'),
    # url(r'^auth/fcm/$', AuthFCMTokenApiView.as_view(), name='fcm-user'),

    url(r'^auth/fcm/$', AuthFCMTokenApiView.as_view(), name='fcm-user'),
    url(r'^auth/facebook/$', AuthFacebookView.as_view()),
    url(r'^auth/check/$', AuthEmailUsernameCheckApiView.as_view(), name='check-user'),
    url(r'^auth/register/facebook/$', FacebookRegisterApiView.as_view(), name='register-facebook'),
]