from rest_framework import serializers

from dcim.api.nested_serializers import NestedManufacturerSerializer, NestedDeviceSerializer
from netbox.api.serializers import NetBoxModelSerializer
from netbox_lifecycle.api.nested_serializers import NestedVendorSerializer
from netbox_lifecycle.models import Vendor, SupportContract


__all__ = (
    'VendorSerializer',
    'SupportContractSerializer',
)


class VendorSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='plugins-api:netbox_lifecycle-api:hardwarelifecycle-detail')

    class Meta:
        model = Vendor
        fields = ('url', 'id', 'display', 'name')


class SupportContractSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='plugins-api:netbox_lifecycle-api:hardwarelifecycle-detail')
    manufacturer = NestedManufacturerSerializer()
    vendor = NestedVendorSerializer()
    start = serializers.DateField()
    renewal = serializers.DateField()
    end = serializers.DateField()
    devices = NestedDeviceSerializer(many=True)

    class Meta:
        model = SupportContract
        fields = ('url', 'id', 'display', 'manufacturer', 'vendor', 'contract_id', 'start', 'renewal', 'end', 'devices')
