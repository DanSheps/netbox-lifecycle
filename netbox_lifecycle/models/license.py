from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.functions import Lower
from django.urls import reverse
from django.utils.translation import gettext as _

from netbox.models import PrimaryModel


__all__ = ('License', 'LicenseAssignment')


class License(PrimaryModel):
    manufacturer = models.ForeignKey(
        to='dcim.Manufacturer',
        on_delete=models.CASCADE,
        related_name='licenses',
    )
    name = models.CharField(max_length=100)

    clone_fields = ('manufacturer',)
    prerequisite_models = ('dcim.Manufacturer',)

    class Meta:
        ordering = ['manufacturer', 'name']
        constraints = (
            models.UniqueConstraint(
                'manufacturer',
                Lower('name'),
                name='%(app_label)s_%(class)s_unique_manufacturer_name',
                violation_error_message="SKU name must be unique per manufacturer.",
            ),
        )

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('plugins:netbox_lifecycle:license', args=[self.pk])


class LicenseAssignment(PrimaryModel):
    license = models.ForeignKey(
        to='netbox_lifecycle.License',
        on_delete=models.CASCADE,
        related_name='assignments',
    )
    vendor = models.ForeignKey(
        to='netbox_lifecycle.Vendor',
        on_delete=models.CASCADE,
        related_name='licenses',
    )
    device = models.ForeignKey(
        to='dcim.Device',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='licenses',
    )
    virtual_machine = models.ForeignKey(
        to='virtualization.VirtualMachine',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='licenses',
    )
    quantity = models.IntegerField(
        null=True,
        blank=True,
    )

    clone_fields = (
        'vendor',
        'license',
    )
    prerequisite_models = (
        'netbox_lifecycle.License',
        'netbox_lifecycle.Vendor',
        'dcim.Device',
        'virtualization.VirtualMachine',
    )

    class Meta:
        ordering = ['license', 'device', 'virtual_machine']
        constraints = (
            models.CheckConstraint(
                check=(
                    models.Q(device__isnull=True, virtual_machine__isnull=False)
                    | models.Q(device__isnull=False, virtual_machine__isnull=True)
                    | models.Q(device__isnull=True, virtual_machine__isnull=True)
                ),
                name='%(app_label)s_%(class)s_device_vm_exclusive',
                violation_error_message=_(
                    'Device and virtual machine are mutually exclusive.'
                ),
            ),
        )

    def __str__(self):
        if self.device:
            return f'{self.device.name}: {self.license.name}'
        if self.virtual_machine:
            return f'{self.virtual_machine.name}: {self.license.name}'
        return f'{self.license.name}'

    def get_absolute_url(self):
        return reverse('plugins:netbox_lifecycle:licenseassignment', args=[self.pk])

    def clean(self):
        super().clean()

        # Mutual exclusivity validation
        if self.device and self.virtual_machine:
            raise ValidationError(
                _('Device and virtual machine are mutually exclusive. Select only one.')
            )

    @property
    def assigned_object(self):
        """Return the device or virtual machine assigned to this license."""
        return self.device or self.virtual_machine

    @property
    def name(self):
        if self.device:
            return self.device.name
        if self.virtual_machine:
            return self.virtual_machine.name
        return None

    @property
    def serial(self):
        if self.device:
            return self.device.serial
        return None  # VMs don't have serial numbers

    @property
    def device_type(self):
        if self.device:
            return self.device.device_type
        return None  # VMs don't have device_type

    @property
    def status(self):
        if self.device:
            return self.device.status
        if self.virtual_machine:
            return self.virtual_machine.status
        return None
