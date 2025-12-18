from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers

from netbox.api.fields import ContentTypeField
from netbox.api.serializers import NetBoxModelSerializer
from netbox_lifecycle.models import HardwareLifecycle


__all__ = ('HardwareLifecycleSerializer',)


class HardwareLifecycleSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_lifecycle-api:hardwarelifecycle-detail'
    )
    assigned_object_type = ContentTypeField(queryset=ContentType.objects.all())

    end_of_sale = serializers.DateField(required=False, allow_null=True)
    end_of_maintenance = serializers.DateField(required=False, allow_null=True)
    end_of_security = serializers.DateField(required=False, allow_null=True)
    last_contract_attach = serializers.DateField(required=False, allow_null=True)
    last_contract_renewal = serializers.DateField(required=False, allow_null=True)
    end_of_support = serializers.DateField(required=False, allow_null=True)

    class Meta:
        model = HardwareLifecycle
        fields = (
            'url',
            'id',
            'display',
            'assigned_object_type',
            'assigned_object_id',
            'end_of_sale',
            'end_of_maintenance',
            'end_of_security',
            'last_contract_attach',
            'last_contract_renewal',
            'end_of_support',
            'notice',
            'documentation',
            'description',
            'comments',
            'tags',
            'custom_fields',
        )
        brief_fields = (
            'url',
            'id',
            'display',
            'assigned_object_type',
            'assigned_object_id',
            'end_of_sale',
        )
