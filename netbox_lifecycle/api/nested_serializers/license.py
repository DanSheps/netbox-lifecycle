from rest_framework import serializers

from dcim.api.nested_serializers import NestedManufacturerSerializer, NestedDeviceSerializer
from netbox.api.serializers import WritableNestedSerializer
from netbox_lifecycle.api.nested_serializers import NestedVendorSerializer
from netbox_lifecycle.models import License, LicenseAssignment

__all__ = (
    'NestedLicenseSerializer',
    'NestedLicenseAssignmentSerializer',
)


class NestedLicenseSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='plugins-api:netbox_lifecycle-api:license-detail')
    manufacturer = NestedManufacturerSerializer()

    class Meta:
        model = License
        fields = ('url', 'id', 'display', 'name', 'manufacturer', )


class NestedLicenseAssignmentSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='plugins-api:netbox_lifecycle-api:licenseassignment-detail')
    license = NestedLicenseSerializer()
    vendor = NestedVendorSerializer()
    device = NestedDeviceSerializer()

    class Meta:
        model = LicenseAssignment
        fields = ('url', 'id', 'display', 'vendor', 'license', 'device')
