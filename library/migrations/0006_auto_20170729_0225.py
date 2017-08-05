# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-29 02:25
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0005_auto_20170729_0142'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'Categories'},
        ),
        migrations.AlterModelOptions(
            name='country',
            options={'verbose_name_plural': 'Countries'},
        ),
        migrations.RenameField(
            model_name='book',
            old_name='title',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='booklist',
            old_name='title',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='category',
            old_name='title',
            new_name='name',
        ),
    ]
