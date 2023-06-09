# Generated by Django 3.0.14 on 2023-06-21 04:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instagram', '0011_auto_20230616_1624'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='tag_set',
            field=models.ManyToManyField(blank=True, to='instagram.Tag'),
        ),
    ]
