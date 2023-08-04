from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('instagram', '0013_auto_20230705_0921'),
    ]

    operations = [
        migrations.DeleteModel(
            name='AI',
        ),
    ]
