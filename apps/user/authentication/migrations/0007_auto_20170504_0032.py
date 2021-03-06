# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-04 00:32
from __future__ import unicode_literals

import apps.core.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0006_user_fcm'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='fcm',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='idsn',
            field=models.CharField(blank=True, db_index=True, max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='photo',
            field=apps.core.fields.ImageField(blank=True, default='default/default.jpg', upload_to='', verbose_name='photo'),
        ),
    ]
