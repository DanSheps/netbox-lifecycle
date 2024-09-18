from rest_framework import serializers

from dcim.api.serializers_.devices import DeviceSerializer
from dcim.api.serializers_.manufacturers import ManufacturerSerializer
from netbox.api.serializers import NetBoxModelSerializer
from netbox_lifecycle.api._serializers.vendor import VendorSerializer
from netbox_lifecycle.models import License, LicenseAssignment

__all__ = (
    'LicenseSerializer',
    'LicenseAssignmentSerializer',
)


class LicenseSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='plugins-api:netbox_lifecycle-api:license-detail')
    manufacturer = ManufacturerSerializer(nested=True)

    class Meta:
        model = License
        fields = ('url', 'id', 'display', 'name', 'manufacturer', 'description', 'comments', )
        brief_fields = ('url', 'id', 'display', 'name', )


class LicenseAssignmentSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='plugins-api:netbox_lifecycle-api:licenseassignment-detail')
    license = LicenseSerializer(nested=True)
    vendor = VendorSerializer(nested=True)
    device = DeviceSerializer(nested=True, required=False, allow_null=True)

    class Meta:
        model = LicenseAssignment
        fields = ('url', 'id', 'display', 'vendor', 'license', 'device', 'description', 'comments', )
        brief_fields = ('url', 'id', 'display', 'vendor', 'license', 'device', )
