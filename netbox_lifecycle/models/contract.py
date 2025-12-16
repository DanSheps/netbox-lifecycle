from datetime import date

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.functions import Lower
from django.urls import reverse
from django.utils.translation import gettext as _

from netbox.models import PrimaryModel

from netbox_lifecycle.constants import (
    CONTRACT_STATUS_ACTIVE,
    CONTRACT_STATUS_EXPIRED,
    CONTRACT_STATUS_FUTURE,
    CONTRACT_STATUS_UNSPECIFIED,
)


__all__ = (
    'Vendor',
    'SupportSKU',
    'SupportContract',
    'SupportContractAssignment',
)


class Vendor(PrimaryModel):
    name = models.CharField(max_length=100)

    clone_fields = ()
    prerequisite_models = ()

    class Meta:
        ordering = ['name']
        constraints = (
            models.UniqueConstraint(
                Lower('name'),
                name='%(app_label)s_%(class)s_unique_name',
                violation_error_message="Vendor must be unique.",
            ),
        )

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('plugins:netbox_lifecycle:vendor', args=[self.pk])


class SupportSKU(PrimaryModel):
    manufacturer = models.ForeignKey(
        to='dcim.Manufacturer',
        on_delete=models.CASCADE,
        related_name='skus',
    )
    sku = models.CharField(max_length=100)

    clone_fields = ('manufacturer',)
    prerequisite_models = ('dcim.Manufacturer',)

    class Meta:
        ordering = ['manufacturer', 'sku']
        constraints = (
            models.UniqueConstraint(
                'manufacturer',
                Lower('sku'),
                name='%(app_label)s_%(class)s_unique_manufacturer_sku',
                violation_error_message="SKU must be unique per manufacturer.",
            ),
        )

    def __str__(self):
        return f'{self.sku}'

    def get_absolute_url(self):
        return reverse('plugins:netbox_lifecycle:supportsku', args=[self.pk])


class SupportContract(PrimaryModel):
    vendor = models.ForeignKey(
        to='netbox_lifecycle.Vendor',
        on_delete=models.SET_NULL,
        related_name='contracts',
        null=True,
        blank=True,
    )
    contract_id = models.CharField(max_length=100)
    start = models.DateField(null=True, blank=True)
    renewal = models.DateField(null=True, blank=True)
    end = models.DateField(null=True, blank=True)

    clone_fields = ('vendor', 'start', 'renewal', 'end')
    prerequisite_models = ('netbox_lifecycle.Vendor',)

    class Meta:
        ordering = ['contract_id']
        constraints = (
            models.UniqueConstraint(
                'vendor',
                Lower('contract_id'),
                name='%(app_label)s_%(class)s_unique_vendor_contract_id',
                violation_error_message="Contract must be unique per vendor.",
            ),
        )

    def __str__(self):
        return f'{self.contract_id}'

    def get_absolute_url(self):
        return reverse('plugins:netbox_lifecycle:supportcontract', args=[self.pk])


class SupportContractAssignment(PrimaryModel):
    contract = models.ForeignKey(
        to='netbox_lifecycle.SupportContract',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assignments',
    )
    sku = models.ForeignKey(
        to='netbox_lifecycle.SupportSKU',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assignments',
    )
    device = models.ForeignKey(
        to='dcim.Device',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='contracts',
    )
    module = models.ForeignKey(
        to='dcim.Module',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='contracts',
    )
    license = models.ForeignKey(
        to='netbox_lifecycle.LicenseAssignment',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='contracts',
    )
    virtual_machine = models.ForeignKey(
        to='virtualization.VirtualMachine',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='contracts',
    )
    end = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('End Date'),
        help_text=_('A unique end date varying from the contract'),
    )

    clone_fields = (
        'contract',
        'sku',
        'module',
        'end',
    )
    prerequisite_models = (
        'netbox_lifecycle.SupportContract',
        'netbox_lifecycle.SupportSKU',
        'netbox_lifecycle.License',
        'dcim.Device',
        'dcim.Module',
        'virtualization.VirtualMachine',
    )

    class Meta:
        ordering = ['contract', 'device', 'virtual_machine', 'module', 'license']
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
        if self.module:
            return f'{self.module}: {self.contract.contract_id}'
        if self.license and self.device:
            return f'{self.device} ({self.license}): {self.contract.contract_id}'
        if self.license and self.virtual_machine:
            return (
                f'{self.virtual_machine} ({self.license}): {self.contract.contract_id}'
            )
        if self.device:
            return f'{self.device}: {self.contract.contract_id}'
        if self.virtual_machine:
            return f'{self.virtual_machine}: {self.contract.contract_id}'
        return f'{self.contract.contract_id}'

    def get_absolute_url(self):
        return reverse(
            'plugins:netbox_lifecycle:supportcontractassignment', args=[self.pk]
        )

    @property
    def end_date(self):
        if self.end:
            return self.end
        return self.contract.end

    @property
    def status(self):
        today = date.today()

        # Check if contract starts in the future
        if self.contract.start and self.contract.start > today:
            return CONTRACT_STATUS_FUTURE

        # Use assignment's end_date property (falls back to contract.end)
        end = self.end_date
        if end is None:
            return CONTRACT_STATUS_UNSPECIFIED
        if end < today:
            return CONTRACT_STATUS_EXPIRED
        return CONTRACT_STATUS_ACTIVE

    def clean(self):
        # Mutual exclusivity: device and virtual_machine
        if self.device and self.virtual_machine:
            raise ValidationError(
                _('Device and virtual machine are mutually exclusive. Select only one.')
            )

        # Module only allowed with device (not with VM)
        if self.module and self.virtual_machine:
            raise ValidationError(
                {
                    'module': _(
                        'Module can only be assigned with a device, not a virtual machine'
                    )
                }
            )

        has_hardware = self.device or self.module or self.virtual_machine
        has_license = self.license

        # Must select something
        if not has_hardware and not has_license:
            raise ValidationError(
                _('Select a device, module, virtual machine, or license assignment')
            )

        # If both device and module, they must match
        if self.device and self.module and self.device != self.module.device:
            raise ValidationError(
                {'module': _('Module must belong to the selected device')}
            )

        # If license has a device, it must match the assignment's device
        if self.license and self.license.device and self.device:
            if self.device != self.license.device:
                raise ValidationError(
                    {
                        'device': _(
                            'Device must match the device assigned to the license'
                        )
                    }
                )

        # If license has a virtual_machine, it must match the assignment's virtual_machine
        if self.license and self.license.virtual_machine and self.virtual_machine:
            if self.virtual_machine != self.license.virtual_machine:
                raise ValidationError(
                    {
                        'virtual_machine': _(
                            'Virtual machine must match the virtual machine assigned to the license'
                        )
                    }
                )

        # Uniqueness check: contract + device + module + virtual_machine + license + sku
        if (
            SupportContractAssignment.objects.filter(
                contract=self.contract,
                device=self.device,
                module=self.module,
                virtual_machine=self.virtual_machine,
                license=self.license,
                sku=self.sku,
            )
            .exclude(pk=self.pk)
            .exists()
        ):
            raise ValidationError(
                _('This assignment combination already exists for this contract')
            )
