# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-05-24 14:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flylo', '0003_auto_20170524_1458'),
    ]

    operations = [
        migrations.AddField(
            model_name='aircraft',
            name='nbussines',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='aircraft',
            name='neconomic',
            field=models.IntegerField(null=True),
        ),
    ]
