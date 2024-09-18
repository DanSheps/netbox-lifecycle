from rest_framework import serializers

from netbox.api.serializers import NetBoxModelSerializer
from netbox_lifecycle.models import Vendor

__all__ = (
    'VendorSerializer',
)


class VendorSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='plugins-api:netbox_lifecycle-api:hardwarelifecycle-detail')

    class Meta:
        model = Vendor
        fields = ('url', 'id', 'display', 'name', 'description', 'comments', )
        brief_fields = ('url', 'id', 'display', 'name', )
