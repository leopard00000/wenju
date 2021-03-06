# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-23 08:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('password', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Items',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wenjuApp.Employee')),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Stationery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('price', models.CharField(max_length=10)),
                ('photo', models.CharField(max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='items',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wenjuApp.Order'),
        ),
        migrations.AddField(
            model_name='items',
            name='stationery',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wenjuApp.Stationery'),
        ),
        migrations.AddField(
            model_name='employee',
            name='section',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wenjuApp.Section'),
        ),
    ]
