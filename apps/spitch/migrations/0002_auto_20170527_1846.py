# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-27 18:46
from __future__ import unicode_literals

import apps.core.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('spitch', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='spitch',
            name='clip_total',
        ),
        migrations.RemoveField(
            model_name='spitch',
            name='clip_uploaded',
        ),
        migrations.AddField(
            model_name='spitch',
            name='spitch',
            field=apps.core.fields.FileField(null=True, upload_to=''),
        ),
    ]
