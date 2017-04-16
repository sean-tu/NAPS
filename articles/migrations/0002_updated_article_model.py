# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-09 03:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0001_added_articles_model'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='category',
            field=models.CharField(blank=True, choices=[('anthropology', 'Anthropology'), ('chemistry', 'Chemistry'), ('computer-science', 'Computer Science'), ('earth-science', 'Earth Science'), ('engineering', 'Engineering'), ('life-science', 'Life Science'), ('materials-science', 'Materials Science'), ('medicine', 'Medicine'), ('mathematics', 'Mathematics'), ('physics', 'Physics')], max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='date_published',
            field=models.IntegerField(blank=True, max_length=4, null=True),
        ),
    ]