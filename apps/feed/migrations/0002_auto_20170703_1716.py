# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-07-03 17:16
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='feed',
            unique_together=set([]),
        ),
    ]
