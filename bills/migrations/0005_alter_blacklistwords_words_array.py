# Generated by Django 3.2.1 on 2021-06-04 16:08

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bills', '0004_blacklistwords'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blacklistwords',
            name='words_array',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=20), blank=True, size=None),
        ),
    ]
