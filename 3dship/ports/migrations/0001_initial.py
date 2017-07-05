# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-07-03 15:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ContainerPosition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('x_position', models.IntegerField(blank=True, null=True, verbose_name='row')),
                ('y_position', models.IntegerField(blank=True, null=True, verbose_name='column')),
                ('z_position', models.IntegerField(blank=True, null=True, verbose_name='height')),
            ],
        ),
        migrations.CreateModel(
            name='Ports',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('port_number', models.IntegerField(blank=True, null=True)),
                ('number_of_containers', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='containerposition',
            name='port',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ports.Ports'),
        ),
    ]
