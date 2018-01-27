import datetime
from django.utils import timezone

from rest_framework import generics
from django.db.models import Q

from .serializers import *
from .pagination import AskListPagination


class AskCreateApiView(generics.CreateAPIView):
    serializer_class = AskCreateSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AskListApiView(generics.ListAPIView):
    serializer_class = AskListSerializer
    pagination_class = AskListPagination

    def get_queryset(self):
        asks = Ask.objects.filter(active=True).filter( Q(receivers__isnull=True) | Q(receivers=self.request.user))
        return asks

    # def get_queryset(self):
    #     search = self.request.query_params.get('search', None)
    #     if search == "hot":
    #         return Ask.objects.filter(receivers__isnull=True).order_by("-created")
    #     if search == "follow":
    #         return Ask.objects.filter(user__followers__user = self.request.user, eceivers__isnull=True)\
    #                 .distinct().order_by("-created")
    #     if search == "private":
    #         return Ask.objects.filter(receivers=self.request.user).order_by("-created")
    #
    #     return Ask.objects.order_by("-created")[:10]


# class TrendTagsListApiView(generics.ListAPIView):
#     serializer_class = TrendTagSerializer
#
#     def get_queryset(self):
#         d =  timezone.now() - datetime.timedelta(days=30)
#         return Tag.objects.filter(asktag__created__gte = d).annotate(ct=Count("tag")).order_by('-ct')[:10]