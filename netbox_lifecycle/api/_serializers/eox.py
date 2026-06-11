from netbox.api.serializers import NetBoxModelSerializer
from rest_framework import serializers

from netbox_lifecycle.models import EoXAPISettings

__all__ = ('EoXAPISettingsSerializer',)


class EoXAPISettingsSerializer(NetBoxModelSerializer):
    url_field = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_lifecycle-api:eoxapisettings-detail'
    )

    class Meta:
        model = EoXAPISettings
        fields = (
            'url_field',
            'id',
            'display',
            'driver',
            'url',
            'manufacturers',
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
            'url_field',
            'id',
            'display',
            'driver',
            'url',
        )
