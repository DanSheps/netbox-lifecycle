from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse

from netbox.models import NetBoxModel


__all__ = (
    'Vendor',
    'SupportContract',
    'SupportContractAssignment',
)


class Vendor(NetBoxModel):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('plugins:netbox_lifecycle:vendor', args=[self.pk])


class SupportContract(NetBoxModel):
    manufacturer = models.ForeignKey(to='dcim.Manufacturer', on_delete=models.CASCADE)
    vendor = models.ForeignKey(to='netbox_lifecycle.Vendor', on_delete=models.CASCADE)
    contract_id = models.CharField(max_length=100)
    start = models.DateField()
    renewal = models.DateField()
    end = models.DateField()

    class Meta:
        ordering = ['contract_id']

    def __str__(self):
        return f'{self.contract_id}'

    def get_absolute_url(self):
        return reverse('plugins:netbox_lifecycle:supportcontract', args=[self.pk])


class SupportContractAssignment(NetBoxModel):
    contract = models.ForeignKey(to='netbox_lifecycle.SupportContract', on_delete=models.CASCADE)

    assigned_object_type = models.ForeignKey(
        to=ContentType,
        limit_choices_to=('dcim.Device', 'netbox_lifecycle.License'),
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

    class Meta:
        ordering = ['contract', 'assigned_object_type', 'assigned_object_id']

    def __str__(self):
        return f'{self.assigned_object}: {self.contract.contract_id}'

    def get_absolute_url(self):
        return reverse('plugins:netbox_lifecycle:supportcontract_assignments', args=[self.contract.pk])