from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
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

    assigned_object_type = models.ForeignKey(
        to=ContentType,
        limit_choices_to=('dcim.Device', 'netbox_lifecycle.LicenseAssignment'),
        on_delete=models.PROTECT,
        related_name='+',
        blank=True,
        null=True
    )
    assigned_object_id = models.PositiveBigIntegerField(
        blank=True,
        null=True
    )
    assigned_object = GenericForeignKey(
        ct_field='assigned_object_type',
        fk_field='assigned_object_id'
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
        ordering = ['contract', 'assigned_object_type', 'assigned_object_id']
        constraints = (
            models.UniqueConstraint(
                'contract', 'sku', 'assigned_object_type', 'assigned_object_id',
                name='%(app_label)s_%(class)s_unique_assignments',
                violation_error_message="Contract assignments must be unique."
            ),
            models.UniqueConstraint(
                'contract', 'assigned_object_type', 'assigned_object_id',
                name='%(app_label)s_%(class)s_unique_assignment_null_sku',
                condition=Q(sku__isnull=True),
                violation_error_message="Contract assignments to assigned_objects must be unique."
            ),
        )

    def __str__(self):
        return f'{self.assigned_object}: {self.contract.contract_id}'

    def get_absolute_url(self):
        return reverse('plugins:netbox_lifecycle:supportcontract_assignments', args=[self.contract.pk])

    @property
    def end_date(self):
        if self.end:
            return self.end
        return self.contract.end

    def get_device_status_color(self):
        if self.assigned_object is None:
            return
        if hasattr(self.assigned_object, 'device'):
            return DeviceStatusChoices.colors.get(self.assigned_object.device.status)
        return DeviceStatusChoices.colors.get(self.assigned_object.status)
