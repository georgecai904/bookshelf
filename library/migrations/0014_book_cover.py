# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-05 15:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0013_auto_20170805_0851'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='cover',
            field=models.FileField(blank=True, upload_to='uploads/%Y/%m/%d'),
        ),
    ]
