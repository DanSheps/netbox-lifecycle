from rest_framework import serializers

from dcim.api.nested_serializers import NestedManufacturerSerializer
from netbox.api.serializers import WritableNestedSerializer
from netbox_lifecycle.models import Vendor, SupportContract

__all__ = (
    'NestedVendorSerializer',
    'NestedSupportContractSerializer',
)


class NestedVendorSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='plugins-api:netbox_lifecycle-api:hardwarelifecycle-detail')

    class Meta:
        model = Vendor
        fields = ('url', 'id', 'display', 'name')


class NestedSupportContractSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='plugins-api:netbox_lifecycle-api:hardwarelifecycle-detail')
    manufactuer = NestedManufacturerSerializer()
    vendor = NestedVendorSerializer()

    class Meta:
        model = SupportContract
        fields = ('url', 'id', 'display', 'contract_id')
