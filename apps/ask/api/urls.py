from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^ask/$', AskCreateApiView.as_view(), name='create-ask'),
    url(r'^ask/list/$', AskListApiView.as_view(), name='swipe-ask'),

    # url(r'^ask/search/$', AskListApiView.as_view(), name='search-ask'),
    # url(r'^trend/tag$', TrendTagsListApiView.as_view(), name='trend-tag'),
]
