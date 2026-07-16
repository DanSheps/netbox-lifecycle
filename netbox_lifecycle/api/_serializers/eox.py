from dcim.api.serializers_.manufacturers import ManufacturerSerializer
from netbox.api.serializers import NetBoxModelSerializer
from rest_framework import serializers

from netbox_lifecycle.models import EoXAPISettings

__all__ = ('EoXAPISettingsSerializer',)


class EoXAPISettingsSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_lifecycle-api:eoxapisettings-detail'
    )
    manufacturer = ManufacturerSerializer(nested=True)

    class Meta:
        model = EoXAPISettings
        fields = (
            'url',
            'id',
            'display',
            'driver',
            'manufacturer',
            'enabled',
            'client_id',
            'sync_interval',
            'last_synced',
            'description',
            'comments',
            'tags',
            'custom_fields',
        )
        brief_fields = (
            'url',
            'id',
            'display',
            'driver',
            'manufacturer',
        )
