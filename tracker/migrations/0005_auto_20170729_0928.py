# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-29 09:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0004_readbook_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='readbook',
            name='status',
            field=models.CharField(choices=[('已读', '已读'), ('在读', '在读'), ('待读', '待读')], default='待读', max_length=2),
        ),
    ]
