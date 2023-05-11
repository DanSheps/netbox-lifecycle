from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse

from dcim.models import DeviceType, ModuleType
from netbox.models import NetBoxModel


__all__ = (
    'Vendor',
    'SupportContract',
    'SupportContractDeviceAssignment',
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


class SupportContractDeviceAssignment(NetBoxModel):
    contract = models.ForeignKey(to='netbox_lifecycle.SupportContract', on_delete=models.CASCADE)
    device = models.ForeignKey(to='dcim.Device', on_delete=models.CASCADE)

    class Meta:
        ordering = ['contract', 'device']

    def __str__(self):
        return f'{self.device.name}: {self.contract.contract_id}'

    def get_absolute_url(self):
        return reverse('plugins:netbox_lifecycle:supportcontract_devices', args=[self.contract.pk])