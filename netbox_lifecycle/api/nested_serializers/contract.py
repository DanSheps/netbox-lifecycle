from rest_framework import serializers

from dcim.api.nested_serializers import NestedManufacturerSerializer
from netbox.api.serializers import WritableNestedSerializer
from netbox_lifecycle.models import Vendor, SupportContract, SupportContractAssignment, SupportSKU

__all__ = (
    'NestedVendorSerializer',
    'NestedSupportSKUSerializer',
    'NestedSupportContractSerializer',
    'NestedSupportContractAssignmentSerializer',
)


class NestedVendorSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='plugins-api:netbox_lifecycle-api:hardwarelifecycle-detail')

    class Meta:
        model = Vendor
        fields = ('url', 'id', 'display', 'name')


class NestedSupportSKUSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='plugins-api:netbox_lifecycle-api:hardwarelifecycle-detail')
    manufacturer = NestedManufacturerSerializer()

    class Meta:
        model = SupportSKU
        fields = ('url', 'id', 'display', 'manufacturer', 'sku')


class NestedSupportContractSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='plugins-api:netbox_lifecycle-api:hardwarelifecycle-detail')
    vendor = NestedVendorSerializer()

    class Meta:
        model = SupportContract
        fields = ('url', 'id', 'display', 'contract_id', 'vendor')


class NestedSupportContractAssignmentSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='plugins-api:netbox_lifecycle-api:licenseassignment-detail')
    contract = NestedSupportContractSerializer()

    class Meta:
        model = SupportContractAssignment
        fields = ('url', 'id', 'display', 'contract', 'device', 'license')
