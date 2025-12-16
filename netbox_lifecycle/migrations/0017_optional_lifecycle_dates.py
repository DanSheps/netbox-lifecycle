from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('netbox_lifecycle', '0016_add_virtual_machine_support'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hardwarelifecycle',
            name='end_of_sale',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='hardwarelifecycle',
            name='end_of_support',
            field=models.DateField(blank=True, null=True),
        ),
    ]
