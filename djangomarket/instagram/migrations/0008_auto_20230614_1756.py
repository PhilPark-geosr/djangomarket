# Generated by Django 3.0.14 on 2023-06-14 08:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('instagram', '0007_auto_20230614_1720'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='image',
            new_name='photo',
        ),
    ]