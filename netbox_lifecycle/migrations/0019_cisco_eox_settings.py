from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('netbox_lifecycle', '0018_netbox_v040500'),
    ]

    operations = [
        migrations.CreateModel(
            name='CiscoEoXSettings',
            fields=[
                (
                    'id',
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('enabled', models.BooleanField(default=False)),
                ('client_id', models.CharField(blank=True, max_length=200)),
                (
                    'client_secret',
                    models.CharField(
                        blank=True, db_column='client_secret', max_length=500
                    ),
                ),
                (
                    'sync_interval',
                    models.PositiveIntegerField(
                        choices=[
                            (60, 'Hourly'),
                            (1440, 'Daily'),
                            (10080, 'Weekly'),
                            (20160, 'Biweekly'),
                            (43200, 'Monthly'),
                        ],
                        default=10080,
                    ),
                ),
                (
                    'manufacturer_names',
                    models.CharField(default='Cisco', max_length=500),
                ),
            ],
            options={
                'verbose_name': 'Cisco EoX Settings',
            },
        ),
    ]
