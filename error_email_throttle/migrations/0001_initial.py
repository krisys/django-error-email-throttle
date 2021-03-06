# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-05-30 09:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ErrorReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stack_trace', models.TextField()),
                ('error_date', models.DateField()),
                ('latest_error', models.DateTimeField(default=django.utils.timezone.now)),
                ('error_count', models.IntegerField(default=0)),
                ('last_emailed', models.DateTimeField(blank=True, null=True)),
                ('function', models.CharField(max_length=100)),
                ('filename', models.CharField(max_length=100)),
                ('lineno', models.IntegerField()),
                ('context_line', models.TextField(blank=True, null=True)),
                ('error_hash', models.CharField(max_length=200, unique=True)),
                ('urls', models.TextField()),
            ],
        ),
    ]
