from rest_framework import serializers

from dcim.api.nested_serializers import NestedManufacturerSerializer, NestedDeviceSerializer
from netbox.api.serializers import NetBoxModelSerializer
from netbox_lifecycle.api.nested_serializers import NestedVendorSerializer, NestedSupportContractSerializer, \
    NestedLicenseAssignmentSerializer
from netbox_lifecycle.models import Vendor, SupportContract, SupportContractAssignment, SupportSKU

__all__ = (
    'VendorSerializer',
    'SupportSKUSerializer',
    'SupportContractSerializer',
    'SupportContractAssignmentSerializer',
)

from utilities.api import get_serializer_for_model


class VendorSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='plugins-api:netbox_lifecycle-api:hardwarelifecycle-detail')

    class Meta:
        model = Vendor
        fields = ('url', 'id', 'display', 'name')


class SupportSKUSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='plugins-api:netbox_lifecycle-api:hardwarelifecycle-detail')
    manufacturer = NestedManufacturerSerializer()

    class Meta:
        model = SupportSKU
        fields = ('url', 'id', 'display', 'manufacturer', 'sku')


class SupportContractSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='plugins-api:netbox_lifecycle-api:hardwarelifecycle-detail')
    vendor = NestedVendorSerializer()
    start = serializers.DateField()
    renewal = serializers.DateField()
    end = serializers.DateField()

    class Meta:
        model = SupportContract
        fields = ('url', 'id', 'display', 'vendor', 'contract_id', 'start', 'renewal', 'end', )


class SupportContractAssignmentSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='plugins-api:netbox_lifecycle-api:licenseassignment-detail')
    contract = NestedSupportContractSerializer()

    device = NestedDeviceSerializer()
    license = NestedLicenseAssignmentSerializer()

    class Meta:
        model = SupportContractAssignment
        fields = (
            'url', 'id', 'display', 'contract', 'device', 'license', 'end'
        )
