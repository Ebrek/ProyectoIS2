# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-10 05:24
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AjustesGeneral',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('froggy_health', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('spider_health', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('spider_speed_x', models.FloatField()),
                ('spider_speed_y', models.FloatField()),
                ('mosquito_health', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('mosquito_speed_x', models.FloatField()),
                ('mosquito_speed_y', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Escenario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('mapa', models.FileField(upload_to='maps/')),
                ('order', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
            ],
        ),
        migrations.CreateModel(
            name='Nivel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('bg_music', models.FileField(upload_to='bg_music/')),
                ('bg_image', models.FileField(upload_to='bg_images/')),
            ],
        ),
        migrations.AddField(
            model_name='escenario',
            name='nivel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Configurador.Nivel'),
        ),
    ]