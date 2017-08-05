# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-29 06:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0006_auto_20170729_0225'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='series',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='subtitle',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
