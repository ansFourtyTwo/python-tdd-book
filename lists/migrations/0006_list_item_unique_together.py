# -*- coding: utf-8 -*-
# Generated by Django 1.11.28 on 2020-05-29 13:26
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0005_rename_item_list_attribute'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='item',
            options={'ordering': ('id',)},
        ),
        migrations.AlterUniqueTogether(
            name='item',
            unique_together=set([('_list', 'text')]),
        ),
    ]