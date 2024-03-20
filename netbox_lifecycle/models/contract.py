from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.db.models.functions import Lower
from django.urls import reverse
from django.utils.translation import gettext as _

from dcim.choices import DeviceStatusChoices
from netbox.models import NetBoxModel


__all__ = (
    'Vendor',
    'SupportSKU',
    'SupportContract',
    'SupportContractAssignment',
)


class Vendor(NetBoxModel):
    name = models.CharField(max_length=100)

    clone_fields = ()
    prerequisite_models = ()

    class Meta:
        ordering = ['name']
        constraints = (
            models.UniqueConstraint(
                Lower('name'),
                name='%(app_label)s_%(class)s_unique_name',
                violation_error_message="Vendor must be unique."
            ),
        )

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('plugins:netbox_lifecycle:vendor', args=[self.pk])


class SupportSKU(NetBoxModel):
    manufacturer = models.ForeignKey(
        to='dcim.Manufacturer',
        on_delete=models.CASCADE,
        related_name='skus',
    )
    sku = models.CharField(max_length=100)

    clone_fields = (
        'manufacturer',
    )
    prerequisite_models = (
        'dcim.Manufacturer',
    )

    class Meta:
        ordering = ['manufacturer', 'sku']
        constraints = (
            models.UniqueConstraint(
                'manufacturer', Lower('sku'),
                name='%(app_label)s_%(class)s_unique_manufacturer_sku',
                violation_error_message="SKU must be unique per manufacturer."
            ),
        )

    def __str__(self):
        return f'{self.sku}'

    def get_absolute_url(self):
        return reverse('plugins:netbox_lifecycle:supportsku', args=[self.pk])


class SupportContract(NetBoxModel):
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

    clone_fields = (
        'vendor', 'start', 'renewal', 'end'
    )
    prerequisite_models = (
        'netbox_lifecycle.Vendor',
    )

    class Meta:
        ordering = ['contract_id']
        constraints = (
            models.UniqueConstraint(
                'vendor', Lower('contract_id'),
                name='%(app_label)s_%(class)s_unique_vendor_contract_id',
                violation_error_message="Contract must be unique per vendor."
            ),
        )

    def __str__(self):
        return f'{self.contract_id}'

    def get_absolute_url(self):
        return reverse('plugins:netbox_lifecycle:supportcontract', args=[self.pk])


class SupportContractAssignment(NetBoxModel):
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
    license = models.ForeignKey(
        to='netbox_lifecycle.LicenseAssignment',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='contracts',
    )
    end = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('End Date'),
        help_text=_('A unique end date varying from the contract')
    )

    clone_fields = (
        'contract', 'sku', 'end',
    )
    prerequisite_models = (
        'netbox_lifecycle.SupportContract',
        'netbox_lifecycle.SupportSKU',
        'netbox_lifecycle.License',
        'dcim.Device',
    )

    class Meta:
        ordering = ['contract', 'device', 'license']
        constraints = ()

    def __str__(self):
        if self.license and self.device:
            return f'{self.device} ({self.license}): {self.contract.contract_id}'
        return f'{self.device}: {self.contract.contract_id}'

    def get_absolute_url(self):
        return reverse('plugins:netbox_lifecycle:supportcontract_assignments', args=[self.contract.pk])

    @property
    def end_date(self):
        if self.end:
            return self.end
        return self.contract.end

    def get_device_status_color(self):
        if self.device is None:
            return
        return DeviceStatusChoices.colors.get(self.device.status)

    def clean(self):
        if self.device and self.license and SupportContractAssignment.objects.filter(
                contract=self.contract, device=self.device, license=self.license, sku=self.sku
        ).exclude(pk=self.pk).count() > 0:
            raise ValidationError('Device or License must be unique')
        elif self.device and not self.license and SupportContractAssignment.objects.filter(
                contract=self.contract, device=self.device, license=self.license
        ).exclude(pk=self.pk).count() > 0:
            raise ValidationError('Device must be unique')
        elif not self.device and self.license and SupportContractAssignment.objects.filter(
                contract=self.contract, device=self.device, license=self.license
        ).exclude(pk=self.pk).count() > 0:
            raise ValidationError('License must be unique')
