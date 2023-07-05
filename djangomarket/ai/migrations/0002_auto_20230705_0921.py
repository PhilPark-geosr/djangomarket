# Generated by Django 3.0.14 on 2023-07-05 00:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ai', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ai',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ai_ai_set', to=settings.AUTH_USER_MODEL),
        ),
    ]
