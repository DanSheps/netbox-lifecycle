from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('virtualization', '0023_squashed_0036'),
        ('netbox_lifecycle', '0015_supportcontractassignment_module'),
    ]

    operations = [
        # Add virtual_machine to LicenseAssignment
        migrations.AddField(
            model_name='licenseassignment',
            name='virtual_machine',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='licenses',
                to='virtualization.virtualmachine',
            ),
        ),
        # Add virtual_machine to SupportContractAssignment
        migrations.AddField(
            model_name='supportcontractassignment',
            name='virtual_machine',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='contracts',
                to='virtualization.virtualmachine',
            ),
        ),
        # Update ordering for LicenseAssignment
        migrations.AlterModelOptions(
            name='licenseassignment',
            options={'ordering': ['license', 'device', 'virtual_machine']},
        ),
        # Update ordering for SupportContractAssignment
        migrations.AlterModelOptions(
            name='supportcontractassignment',
            options={
                'ordering': [
                    'contract',
                    'device',
                    'virtual_machine',
                    'module',
                    'license',
                ]
            },
        ),
        # Remove old constraint from LicenseAssignment if it exists
        migrations.RemoveConstraint(
            model_name='licenseassignment',
            name='netbox_lifecycle_licenseassignment_unique_license_vendor_device',
        ),
        # Add check constraint for mutual exclusivity in LicenseAssignment
        migrations.AddConstraint(
            model_name='licenseassignment',
            constraint=models.CheckConstraint(
                check=models.Q(device__isnull=True, virtual_machine__isnull=False)
                | models.Q(device__isnull=False, virtual_machine__isnull=True)
                | models.Q(device__isnull=True, virtual_machine__isnull=True),
                name='netbox_lifecycle_licenseassignment_device_vm_exclusive',
                violation_error_message='Device and virtual machine are mutually exclusive.',
            ),
        ),
        # Add check constraint for mutual exclusivity in SupportContractAssignment
        migrations.AddConstraint(
            model_name='supportcontractassignment',
            constraint=models.CheckConstraint(
                check=models.Q(device__isnull=True, virtual_machine__isnull=False)
                | models.Q(device__isnull=False, virtual_machine__isnull=True)
                | models.Q(device__isnull=True, virtual_machine__isnull=True),
                name='netbox_lifecycle_supportcontractassignment_device_vm_exclusive',
                violation_error_message='Device and virtual machine are mutually exclusive.',
            ),
        ),
    ]
