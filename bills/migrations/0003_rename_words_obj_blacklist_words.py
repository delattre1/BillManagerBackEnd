# Generated by Django 3.2.1 on 2021-06-04 16:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bills', '0002_rename_words_array_blacklist_words_obj'),
    ]

    operations = [
        migrations.RenameField(
            model_name='blacklist',
            old_name='words_obj',
            new_name='words',
        ),
    ]