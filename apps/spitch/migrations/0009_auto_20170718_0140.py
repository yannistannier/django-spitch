# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-07-18 01:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spitch', '0008_spitch_spitch_transcoded'),
    ]

    operations = [
        migrations.AlterField(
            model_name='spitch',
            name='active',
            field=models.BooleanField(db_index=True, default=False),
        ),
    ]
