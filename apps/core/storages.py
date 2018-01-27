# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.conf import settings

from storages.backends.s3boto3 import S3Boto3Storage

StaticStorage = lambda: S3Boto3Storage(location=settings.STATICFILES_LOCATION)  # noqa
# MediaStorage = lambda: S3Boto3Storage(location=settings.MEDIAFILES_LOCATION, object_parameters={'Metadata' : settings.AWS_META_DATA})
MediaStorage = lambda: S3Boto3Storage(location=settings.MEDIAFILES_LOCATION)


