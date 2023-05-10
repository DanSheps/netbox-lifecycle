from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse

from dcim.models import DeviceType, ModuleType
from netbox.models import NetBoxModel


__all__ = (
    'License',
    'LicenseAssignment'
)

class License(NetBoxModel):
    manufacturer = models.ForeignKey(to='dcim.Manufacturer', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ['manufacturer', 'name']

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('plugins:netbox_lifecycle:license', args=[self.pk])


class LicenseAssignment(NetBoxModel):
    license = models.ForeignKey(to='netbox_lifecycle.License', on_delete=models.CASCADE)
    vendor = models.ForeignKey(to='netbox_lifecycle.Vendor', on_delete=models.CASCADE)
    device = models.ForeignKey(to='dcim.Device', on_delete=models.CASCADE)

    class Meta:
        ordering = ['license', 'device']

    def __str__(self):
        return f'{self.device.name}: {self.license.name}'

    def get_absolute_url(self):
        return reverse('plugins:netbox_lifecycle:license_assignments', args=[self.license.pk])
