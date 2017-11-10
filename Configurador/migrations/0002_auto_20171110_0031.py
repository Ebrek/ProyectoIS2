# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-10 05:31
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Configurador', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ajustesgeneral',
            name='mosquito_speed_x',
            field=models.FloatField(validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='ajustesgeneral',
            name='mosquito_speed_y',
            field=models.FloatField(validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='ajustesgeneral',
            name='spider_speed_x',
            field=models.FloatField(validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='ajustesgeneral',
            name='spider_speed_y',
            field=models.FloatField(validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
