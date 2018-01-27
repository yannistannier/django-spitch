# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import os
import uuid

from django.db import models

class ImageField(models.ImageField):

    def generate_filename(self, instance, filename):
        identity = str(instance.id)
        model_field_name = str(self.name)
        filename, extension = os.path.splitext(filename)
        filename = str(uuid.uuid4()).replace("-", "")[:20] + str(extension).lower()
        return '{}/{}/{}'.format(identity, model_field_name, filename)


class FileField(models.FileField):

    def generate_filename(self, instance, filename):
        identity = str(instance.id)
        user = str(instance.user.id)
        model_field_name = str(self.name)
        filename, extension = os.path.splitext(filename)
        filename = str(uuid.uuid4()).replace("-", "")[:20] + str(extension).lower()
        return '{}/{}/{}/{}'.format(user, model_field_name, identity, filename)