# Generated by Django 3.1 on 2023-07-06 08:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ai', '0003_auto_20230706_0857'),
    ]

    operations = [
        migrations.CreateModel(
            name='InferenceModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='AIDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(blank=True, upload_to='ai/detail//%Y/%m/%d')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('result', models.JSONField()),
                ('model_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ai.inferencemodel')),
                ('task_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ai.task')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ai_aidetail_set', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
    ]