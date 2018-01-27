from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^worker/$', WorkerApiView.as_view(), name='worker')
]