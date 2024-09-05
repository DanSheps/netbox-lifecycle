from rest_framework import serializers

from dcim.api.serializers_.devices import DeviceSerializer
from dcim.api.serializers_.manufacturers import ManufacturerSerializer
from netbox.api.serializers import NetBoxModelSerializer
from netbox_lifecycle.api._serializers.license import LicenseAssignmentSerializer
from netbox_lifecycle.api._serializers.vendor import VendorSerializer
from netbox_lifecycle.models import Vendor, SupportContract, SupportContractAssignment, SupportSKU

__all__ = (
    'SupportSKUSerializer',
    'SupportContractSerializer',
    'SupportContractAssignmentSerializer',
)


class SupportSKUSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='plugins-api:netbox_lifecycle-api:hardwarelifecycle-detail')
    manufacturer = ManufacturerSerializer(nested=True)

    class Meta:
        model = SupportSKU
        fields = ('url', 'id', 'display', 'manufacturer', 'sku')


class SupportContractSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='plugins-api:netbox_lifecycle-api:hardwarelifecycle-detail')
    vendor = VendorSerializer(nested=True)
    start = serializers.DateField()
    renewal = serializers.DateField()
    end = serializers.DateField()

    class Meta:
        model = SupportContract
        fields = ('url', 'id', 'display', 'vendor', 'contract_id', 'start', 'renewal', 'end', )


class SupportContractAssignmentSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='plugins-api:netbox_lifecycle-api:licenseassignment-detail')
    contract = SupportContractSerializer(nested=True)

    device = DeviceSerializer(nested=True)
    license = LicenseAssignmentSerializer(nested=True)

    class Meta:
        model = SupportContractAssignment
        fields = (
            'url', 'id', 'display', 'contract', 'device', 'license', 'end'
        )
