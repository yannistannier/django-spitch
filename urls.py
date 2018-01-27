import os
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.http import HttpResponse

urlpatterns = [
    url(r'^api/', include([
        url(r'^', include('apps.authentication.urls')),
        url(r'^', include('apps.relation.urls')),
        url(r'^', include('apps.ask.urls')),
        url(r'^', include('apps.user.urls')),
        url(r'^', include('apps.notification.urls')),
        url(r'^', include('apps.spitch.urls')),
        url(r'^', include('apps.feed.urls')),
    ])),
    url(r'^admin/', admin.site.urls),
    url(r"^health/", lambda r: HttpResponse())
]


if os.environ["DJANGO_SETTINGS_MODULE"] == "settings.worker" or settings.DEBUG :
    urlpatterns += [
        url(r'^', include('apps.worker.urls')),
    ]
