# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-24 12:58
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('flylo', '0002_auto_20170520_2011'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=2, null=True)),
                ('bought', models.BooleanField(default=False)),
                ('checked', models.BooleanField(default=False)),
                ('seats', models.IntegerField(null=True)),
                ('price', models.FloatField(null=True)),
                ('idseats', models.CharField(default='', max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='shoppingcart',
            name='user',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='shop', to='flylo.Client'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='client',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='client', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='item',
            name='cart',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flylo.ShoppingCart'),
        ),
        migrations.AddField(
            model_name='item',
            name='flight',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flylo.Flight'),
        ),
    ]
