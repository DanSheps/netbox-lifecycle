# Generated manually for feature/85-120-module-assignment

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dcim', '0185_gfk_indexes'),
        ('netbox_lifecycle', '0014_rename_last_contract_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='supportcontractassignment',
            name='module',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='contracts',
                to='dcim.module',
            ),
        ),
        migrations.AlterModelOptions(
            name='supportcontractassignment',
            options={'ordering': ['contract', 'device', 'module', 'license']},
        ),
    ]
