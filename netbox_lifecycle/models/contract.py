from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse

from dcim.models import DeviceType, ModuleType
from netbox.models import NetBoxModel


__all__ = (
    'Vendor',
    'SupportContract',
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
    devices = models.ManyToManyField(
        to='dcim.Device',
        related_name='contracts',
        blank=True
    )

    class Meta:
        ordering = ['contract_id']

    def __str__(self):
        return f'{self.contract_id}'

    def get_absolute_url(self):
        return reverse('plugins:netbox_lifecycle:supportcontract', args=[self.pk])